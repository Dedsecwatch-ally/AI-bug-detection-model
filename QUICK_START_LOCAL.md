# 🚀 Quick Start - AI Bug Finder (Local Deployment)

Your AI Bug Finder is now **fully trained and ready to use locally** with a fine-tuned model!

## What's Included

✅ **Fine-tuned GPT-2 model** (125M parameters) trained on 20 code review examples  
✅ **FastAPI backend** with `/review` endpoint  
✅ **React frontend** (Vite) with code editor and review display  
✅ **VS Code extension** for quick code reviews  
✅ **Static analysis** with pylint integration  

---

## Prerequisites

Make sure you have:
- Python 3.8+ with venv (already set up at `/Users/ayushmansingh/py/.venv`)
- Node.js + npm (for web-ui)
- All training dependencies installed (torch, transformers, etc.)

---

## 🏃 Start the Full Stack (3 Simple Steps)

### Step 1: Start the Backend (Terminal 1)

```bash
cd /Users/ayushmansingh/py/ai-bug-finder

PYTHONPATH=/Users/ayushmansingh/py/ai-bug-finder \
/Users/ayushmansingh/py/.venv/bin/python -m uvicorn backend.src.app:app --port 8000
```

**Expected output:**
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ Backend ready on `http://localhost:8000`

---

### Step 2: Start the Frontend (Terminal 2)

```bash
cd /Users/ayushmansingh/py/ai-bug-finder/web-ui

npm run dev
```

**Expected output:**
```
  ➜  Local:   http://localhost:5173/
```

✅ Frontend ready on `http://localhost:5173`

---

### Step 3: Open the App

Go to **http://localhost:5173** in your browser and:
1. Paste Python code into the editor
2. Click "Review Code"
3. See your fine-tuned model's review!

---

## 📝 Test the Backend Directly

While the backend is running, test it with curl:

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo():\n    x = 10\n    return x"}'
```

**Expected response:**
```json
{
  "review": "[Generated review from fine-tuned model]",
  "static_report": "[Pylint analysis results]",
  "patches": [...],
  "full_file": "..."
}
```

---

## 🧠 Your Fine-Tuned Model

**Location:** `backend/fine_tuned_model_small/`  
**Base Model:** GPT-2 (124M parameters)  
**Training Data:** 20 code review examples  
**Framework:** HuggingFace Transformers + LoRA  

The model was trained to understand:
- Bug detection (unused variables, logic errors)
- Security issues (hardcoded passwords, eval() usage)
- Code style improvements
- Performance concerns

### Improve the Model

To train on more examples:

```bash
# 1. Add more examples to backend/training_data.json
# 2. Run the training script again
cd /Users/ayushmansingh/py/ai-bug-finder/backend

/Users/ayushmansingh/py/.venv/bin/python train_small.py
```

The model will be updated and ready to use immediately.

---

## 📊 Configuration

### Use a Different Model

Edit `backend/src/model.py` and change the `MODEL_NAME`:

```python
# Use Phi-3 (better quality, requires GPU):
MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"

# Use fine-tuned GPT-2 (current, works on CPU):
MODEL_NAME = "./fine_tuned_model_small"

# Or set via environment variable:
BUG_MODEL=microsoft/phi-3-mini-4k-instruct python -m uvicorn ...
```

### Adjust Review Parameters

In `backend/src/model.py`, modify:

```python
# Temperature: 0.4 = focused, higher = more creative
temperature=0.4,

# top_p: 0.9 = diverse, lower = deterministic
top_p=0.9,

# max_new_tokens: More = longer reviews
max_new_tokens=400,
```

### Use Gemini API (Cloud)

```bash
export GEMINI_API_KEY="your-api-key-here"
export GEMINI_MODEL="models/text-bison-001"

# Restart backend - it will use Gemini instead of local model
PYTHONPATH=/Users/ayushmansingh/py/ai-bug-finder \
/Users/ayushmansingh/py/.venv/bin/python -m uvicorn backend.src.app:app --port 8000
```

---

## 🔍 API Endpoints

### POST /review
Generate a code review.

**Request:**
```json
{
  "code": "def foo():\n    x = 10\n    return x"
}
```

**Response:**
```json
{
  "review": "Issue: Unused variable x. ...",
  "static_report": "unused-variable (W0612): Unused variable 'x'",
  "patches": [...],
  "full_file": "..."
}
```

### GET /docs
Interactive API documentation (Swagger UI)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure PYTHONPATH is set correctly
cd /Users/ayushmansingh/py/ai-bug-finder

PYTHONPATH=/Users/ayushmansingh/py/ai-bug-finder \
/Users/ayushmansingh/py/.venv/bin/python -m uvicorn backend.src.app:app --port 8000
```

### Port 8000 already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use a different port
... --port 8001
```

### Model loading errors
```bash
# Make sure you're in the backend directory
cd backend

# The fine-tuned model should be in: ./fine_tuned_model_small/
ls -la fine_tuned_model_small/

# If missing, retrain:
/Users/ayushmansingh/py/.venv/bin/python train_small.py
```

### Frontend not connecting to backend
1. Make sure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify API calls in Network tab
4. Try the `/docs` endpoint: http://localhost:8000/docs

---

## 📁 Directory Structure

```
ai-bug-finder/
├── backend/
│   ├── src/
│   │   ├── app.py           # FastAPI endpoints
│   │   ├── model.py         # Model loading & inference
│   │   ├── analysis.py      # Pylint integration
│   │   └── utils.py         # Utilities
│   ├── fine_tuned_model_small/  # Your trained model ✨
│   ├── training_data.json   # Training examples
│   ├── train_small.py       # Training script
│   └── requirements-train.txt
├── web-ui/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── components/      # UI components
│   │   └── api.js           # API client
│   ├── package.json
│   └── vite.config.js
├── vscode-extension/        # VS Code integration
└── QUICK_START_LOCAL.md     # This file!
```

---

## 🎯 Next Steps

### Improve Your Model
- Add more training examples to `backend/training_data.json`
- Retrain with `python train_small.py`
- Test with your code review cases

### Deploy to Production
- Use a larger model (Mistral, Phi-3) on GPU for better quality
- Deploy to cloud (AWS, Azure, GCP)
- Set up CI/CD pipeline
- Add authentication and rate limiting

### Integrate with Your Workflow
- Install the VS Code extension
- Add GitHub Actions to review PRs
- Integrate with Slack or Discord
- Use the API in your IDE

---

## 📚 More Information

- **Full API docs:** http://localhost:8000/docs (when backend is running)
- **Training guide:** See `backend/train_small.py`
- **Model info:** `backend/fine_tuned_model_small/`

---

## 💡 Tips

1. **Keep training data updated:** Add new bug patterns your team finds
2. **Monitor performance:** Check that reviews make sense for your codebase
3. **Adjust parameters:** Try different temperature/top_p values for your use case
4. **Consider GPU:** If you have CUDA/MPS, training and inference will be much faster

---

**🎉 You're all set! Start with Step 1 above and you'll be reviewing code with AI in seconds.**
