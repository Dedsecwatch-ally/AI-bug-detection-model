# Backend README
This backend serves the AI Bug Finder code review API.

Configuration
 - BUG_MODEL: (optional) Hugging Face model name to load locally. If omitted, the code will attempt to use the Gemini API if configured.
 - GEMINI_API_KEY or GOOGLE_API_KEY: (optional) If set, backend will call Google Generative (Gemini) API for review generation. This provides higher-quality, instruction-following responses but requires network and API key.
 - GEMINI_MODEL: (optional) defaults to `models/text-bison-001`. Set to other Gemini model resource names as needed.

Example (use Gemini):

```bash
export GOOGLE_API_KEY="<your-key>"
export GEMINI_MODEL="models/text-bison-001"
uvicorn backend.src.app:app --reload --port 8000
```

If Gemini is not configured, the service falls back to loading a Hugging Face model specified by `BUG_MODEL`. Loading transformer models requires `transformers` and `torch` and can be resource heavy.
