# model.py
import os
from typing import Optional, Any
import json


# Use locally fine-tuned model (trained on code review examples)
# Falls back to Phi-3-mini if not available
MODEL_NAME = os.getenv("BUG_MODEL", "./fine_tuned_model_small")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/text-bison-001")

# Lazy-loaded globals
_tokenizer: Optional[Any] = None
_model: Optional[Any] = None
_device: Optional[Any] = None


def _choose_device():
    # Prefer CUDA, then MPS, then CPU. Import torch lazily so module import
    # doesn't fail when torch isn't installed (useful for tests).
    try:
        import torch as _torch
    except Exception:
        return "cpu"

    if _torch.cuda.is_available():
        return _torch.device("cuda")
    if hasattr(_torch.backends, "mps") and _torch.backends.mps.is_available():
        return _torch.device("mps")
    return _torch.device("cpu")


def _ensure_model():
    global _tokenizer, _model, _device
    if _model is not None and _tokenizer is not None:
        return
    _device = _choose_device()
    # Import transformers lazily so importing this module doesn't require the
    # transformers package to be installed (useful for tests and dev mode).
    from transformers import AutoTokenizer, AutoModelForCausalLM

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    try:
        # Move model to device if torch is available and device is a torch.device
        import torch as _torch
        if isinstance(_device, _torch.device):
            _model.to(_device)
    except Exception:
        # If moving to device fails or torch isn't available, fall back to CPU
        _device = "cpu"


def _generate_review_gemini(prompt: str, max_new_tokens: int = 400) -> str:
    """Call Google Generative API (Gemini/text-bison) using REST.

    Expects GEMINI_API_KEY or GOOGLE_API_KEY in env. GEMINI_MODEL can be set to
    a model resource name such as `models/text-bison-001`.
    """
    api_key = GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("Gemini API key not configured (set GEMINI_API_KEY or GOOGLE_API_KEY)")

    url = f"https://generativelanguage.googleapis.com/v1beta2/{GEMINI_MODEL}:generate?key={api_key}"

    try:
        import requests
    except Exception:
        raise RuntimeError("requests library required for Gemini integration. Install with `pip install requests`")

    payload = {
        "prompt": {"text": prompt},
        "maxOutputTokens": int(max_new_tokens)
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"Gemini request failed: {e}")

    if resp.status_code != 200:
        # try to include body for debugging
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")

    data = resp.json()
    # v1beta2 returns 'candidates' array with 'content'
    if isinstance(data, dict):
        if 'candidates' in data and len(data['candidates']) > 0:
            return data['candidates'][0].get('content', '')
        if 'output' in data and isinstance(data['output'], str):
            return data['output']
        # fallback: stringify a likely text field
        for k in ('text', 'response', 'result'):
            if k in data:
                return json.dumps(data[k])

    return str(data)


def generate_review(prompt: str, max_new_tokens: int = 400):
    """Generate a review from the configured model.

    Priority order:
    - If Gemini API key is present (GEMINI_API_KEY or GOOGLE_API_KEY), use Gemini.
    - Otherwise, lazily load the local transformer model (existing behavior).
    """
    # If configured, use Gemini (cloud API) for higher-quality generation
    if GEMINI_API_KEY:
        return _generate_review_gemini(prompt, max_new_tokens)

    # Fallback to local HF model. If transformers/torch are not installed or
    # model loading fails, return a safe dev-mode review so the service can be
    # used for integration testing without heavy ML dependencies.
    try:
        _ensure_model()
    except Exception as e:
        # Dev fallback review message
        return (
            "[DEV REVIEW] Model unavailable: "
            + str(e)
            + "\n\nThis is a fallback review used for development."
        )

    assert _tokenizer is not None and _model is not None and _device is not None

    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    # Only move tensors if device is a torch.device
    try:
        import torch as _torch
        if isinstance(_device, _torch.device):
            inputs = {k: v.to(_device) for k, v in inputs.items()}
    except Exception:
        # torch not available or device is 'cpu' string — skip
        pass

    outputs = _model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.4,
        do_sample=True,
        top_p=0.9,
    )
    return _tokenizer.decode(outputs[0], skip_special_tokens=True)