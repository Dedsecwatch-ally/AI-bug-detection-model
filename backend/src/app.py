# app.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import generate_review, GEMINI_API_KEY
import json
import re
from .analysis import run_static_analysis

app = FastAPI(title="AI Bug Finder & Code Reviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    code: str


MAX_CODE_LENGTH = 20000


@app.post("/review")
def review_code(req: ReviewRequest):
    # Basic validation
    if not req.code or not isinstance(req.code, str):
        raise HTTPException(status_code=400, detail="Missing code in request")
    if len(req.code) > MAX_CODE_LENGTH:
        raise HTTPException(status_code=413, detail="Code payload too large")

    # Run static checks
    static_report = run_static_analysis(req.code)

    # Compose prompt for model
    # If Gemini is configured, ask it to return a strict JSON document with
    # machine-readable patches. Otherwise ask for a text review.
    if GEMINI_API_KEY:
        prompt = f"""
You are an expert code reviewer and patch generator.
Analyze the following Python code for logical errors, bugs, bad practices, and improvements.
Return JSON only, no additional text. The JSON must have the following shape:
{
  "review": string,            // human-readable summary
  "patches": [                // array of edit operations; may be empty
    {"op":"replace_line", "line": <1-based line number>, "content": "..."},
    {"op":"replace_range", "start": <1-based start>, "end": <1-based end>, "content": "..."}
  ],
  "full_file": null|string     // optional full-file replacement as a string
}

Code:
{req.code}

Static analysis (pylint):
{static_report}

If you cannot produce patches, return an empty patches array and still include a review string.
"""
    else:
        prompt = f"""You are an expert code reviewer.
Analyze the following Python code for logical errors, bugs, bad practices, and improvements.
Then summarize your findings.

Code:
{req.code}

Static analysis (pylint):
{static_report}

Please provide a concise, numbered list of issues and suggested fixes.
"""

    try:
        review_text = generate_review(prompt, max_new_tokens=800)
    except Exception as e:
        # Return the error text during local debugging to help diagnose issues.
        raise HTTPException(status_code=500, detail=f"Model generation error: {e}")

    # If Gemini was used, try to parse JSON from the review_text and return
    # structured patches to the client.
    result_payload = {"review": review_text, "static_report": static_report}
    if GEMINI_API_KEY and isinstance(review_text, str):
        # Try direct JSON decode first
        decoded = None
        try:
            decoded = json.loads(review_text)
        except Exception:
            # Attempt to extract the first JSON object from the text
            m = re.search(r"(\{[\s\S]*\})", review_text)
            if m:
                try:
                    decoded = json.loads(m.group(1))
                except Exception:
                    decoded = None

        if isinstance(decoded, dict):
            # Normalize fields
            result_payload['review'] = decoded.get('review', result_payload['review'])
            result_payload['patches'] = decoded.get('patches', [])
            if 'full_file' in decoded:
                result_payload['full_file'] = decoded.get('full_file')

    return result_payload