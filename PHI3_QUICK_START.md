# 🚀 Phi-3-Mini Quick Start Guide

## What's New

Your backend now uses **Microsoft Phi-3-Mini** instead of Ollama. No external services needed!

---

## ⚡ Quick Command

**Copy & paste this to start the backend:**

```bash
cd /Users/ayushmansingh/py/ai-bug-finder && PYTHONPATH=$(pwd) /Users/ayushmansingh/py/ai-bug-finder/backend/venv/bin/python -m uvicorn backend.src.app:app --port 8000
```

That's it! Server runs on http://localhost:8000

---

## 30-Second Setup

### 1. Install (Already Done ✓)
```bash
# Already installed:
# - torch==2.9.0
# - transformers==4.57.1
```

### 2. Start Backend
```bash
cd /Users/ayushmansingh/py/ai-bug-finder

PYTHONPATH=$(pwd) /Users/ayushmansingh/py/ai-bug-finder/backend/venv/bin/python -m uvicorn backend.src.app:app --port 8000
```

**First time:** Wait 2-5 minutes for model download
**After that:** Loads in 5-10 seconds

### 3. Test It
```bash
# In another terminal
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo():\n    return 42"}'
```

### 4. Open Frontend
```bash
cd /Users/ayushmansingh/py/ai-bug-finder/web-ui
npm run dev
# Visit http://localhost:5173
```

---

## Parameters (Optional)

All configurable via environment variables:

```bash
# Focused reviews (precise, short)
PHI_TEMPERATURE=0.2
PHI_TOP_P=0.8
PHI_MAX_NEW_TOKENS=250

# Creative reviews (detailed, varied)
PHI_TEMPERATURE=0.7
PHI_TOP_P=0.95
PHI_MAX_NEW_TOKENS=500

# Quick reviews (fast, brief)
PHI_MAX_NEW_TOKENS=150
```

**Use them:**
```bash
PHI_TEMPERATURE=0.2 python -m uvicorn backend.src.app:app --port 8000
```

---

## Expected Performance

| Device | Speed | Inference Time |
|--------|-------|-----------------|
| GPU (CUDA) | ⚡ Fast | 3-10 seconds |
| CPU | 🐢 Slow | 30-120 seconds |

Check your device:
```bash
python -c "import torch; print('GPU' if torch.cuda.is_available() else 'CPU')"
```

---

## Troubleshooting

### Model downloading (slow/stuck)
✓ **Normal** - 7.4GB download, 2-5 minutes
- Keep internet connected
- Model auto-caches to `~/.cache/huggingface/hub/`

### Out of memory
```bash
# Use CPU (slower but works everywhere)
# Edit backend/src/model.py: DEVICE = "cpu"

# Or reduce response length
PHI_MAX_NEW_TOKENS=150
```

### "Module not found" error
```bash
pip install torch transformers
```

---

## Key Files Modified

| File | Change |
|------|--------|
| `backend/src/model.py` | ✅ Ollama → Phi-3-Mini |
| `backend/requirements.txt` | ✅ Added torch + transformers |
| `backend/src/app.py` | ⚪ No change |
| `web-ui/*` | ⚪ No change |

---

## Removing Ollama

You can now safely remove Ollama:
```bash
# If you installed it, uninstall it
brew uninstall ollama

# Or just don't run "ollama serve"
# The backend no longer needs it
```

---

## Configuration Examples

### Preset 1: Focused (Best for Bug Detection)
```bash
export PHI_TEMPERATURE=0.2
export PHI_TOP_P=0.8
export PHI_TOP_K=20
export PHI_MAX_NEW_TOKENS=300

python -m uvicorn backend.src.app:app --port 8000
```

### Preset 2: Balanced (Recommended)
```bash
export PHI_TEMPERATURE=0.4
export PHI_TOP_P=0.9
export PHI_TOP_K=40
export PHI_MAX_NEW_TOKENS=300

python -m uvicorn backend.src.app:app --port 8000
```

### Preset 3: Creative (Best for Details)
```bash
export PHI_TEMPERATURE=0.7
export PHI_TOP_P=0.95
export PHI_TOP_K=50
export PHI_MAX_NEW_TOKENS=500

python -m uvicorn backend.src.app:app --port 8000
```

### Preset 4: Quick (Fastest)
```bash
export PHI_TEMPERATURE=0.3
export PHI_MAX_NEW_TOKENS=150

python -m uvicorn backend.src.app:app --port 8000
```

---

## Single Command Start

```bash
cd /Users/ayushmansingh/py/ai-bug-finder && \
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8000
```

That's it! 🎉

---

## What Changed Under the Hood

```python
# Before (Ollama)
requests.post("http://localhost:11434/api/generate", ...)

# After (Phi-3-Mini)
model.generate(input_ids, max_new_tokens=300, ...)
```

**Benefits:**
✅ No external service needed
✅ Faster on GPU (3-10s vs 30-60s)
✅ Runs locally, no API keys
✅ Same simple interface

---

## Next Steps

1. **Start the backend** (see above)
2. **Wait for first-time model download** (~2-5 min)
3. **Test with sample code**
4. **(Optional) Adjust parameters** based on results
5. **Deploy** with your preferred settings

---

**Questions?** See the documentation in this repo for details.

**Ready?** Let's go! 🚀
