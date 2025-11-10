# 🚀 Full Stack Setup Guide

This guide walks you through running the complete AI Bug Finder application (backend + frontend + Ollama).

## Architecture

```
┌─────────────────────────────────────────┐
│         Web UI (React + Vite)           │
│         http://localhost:5173           │
└────────────────┬────────────────────────┘
                 │ HTTP requests (axios)
                 ↓
┌─────────────────────────────────────────┐
│       FastAPI Backend                   │
│       http://localhost:8000             │
│  - /review endpoint                     │
│  - Static analysis (pylint)             │
└────────────────┬────────────────────────┘
                 │ HTTP requests
                 ↓
┌─────────────────────────────────────────┐
│      Ollama Service                     │
│      http://localhost:11434             │
│  - LLM inference (granite3.1-dense)     │
└─────────────────────────────────────────┘
```

## Prerequisites

- **Ollama** installed and a model downloaded
- **Node.js 18+** for the frontend
- **Python 3.8+** for the backend
- All dependencies installed (npm install, pip install)

## Running the Full Stack

### Terminal 1: Start Ollama Server
```bash
ollama serve
```
This starts the Ollama API on `http://localhost:11434`

### Terminal 2: Start Backend
```bash
cd backend
source venv/bin/activate
OLLAMA_MODEL=granite3.1-dense python -m uvicorn src.app:app --port 8000
```
Backend runs on `http://localhost:8000`

### Terminal 3: Start Frontend
```bash
cd web-ui
npm run dev
# or: npx vite
```
Frontend runs on `http://localhost:5173`

## ✅ Verify Everything Works

### 1. Check Ollama
```bash
curl http://localhost:11434/api/tags
# Should list your models
```

### 2. Test Backend Endpoint
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo():\n    x = 10\n    return x"}'
```

### 3. Open Frontend
Navigate to `http://localhost:5173` and click "Review Code"

## API Endpoints

### POST /review
Reviews Python code using Ollama and static analysis.

**Request:**
```json
{
  "code": "def foo():\n    return 42"
}
```

**Response:**
```json
{
  "review": "Code review from Ollama model...",
  "static_report": "Pylint analysis output..."
}
```

## Frontend Features

- **Code Editor**: Monaco Editor with Python syntax highlighting
- **Real-time Review**: Click "Review Code" to analyze
- **Static Analysis**: Pylint results displayed
- **Code Suggestions**: View and apply suggested patches (if available)
- **Error Handling**: Graceful error messages

## Customization

### Change the Model
Set `OLLAMA_MODEL` environment variable:
```bash
OLLAMA_MODEL=llama2 python -m uvicorn src.app:app --port 8000
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000
OLLAMA_MODEL=codellama python -m uvicorn src.app:app --port 8000
```

### Change Backend Port
```bash
python -m uvicorn src.app:app --port 9000
```

Then update frontend `.env`:
```
VITE_API_URL=http://localhost:9000
```

### Change Frontend Port
```bash
npx vite --port 3000
```

## Troubleshooting

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check `.env` has correct `VITE_API_URL`
- Check browser console for CORS errors

### Backend errors
- Check Ollama is running: `curl http://localhost:11434/api/tags`
- Ensure model exists: `ollama list`
- Check env vars: `echo $OLLAMA_MODEL`

### Slow responses
- Use a smaller/faster model (Mistral instead of Llama 2 13B)
- Reduce `max_new_tokens` in `backend/src/app.py` (currently 800)
- Check system resources

## Production Deployment

See individual README files for each component:
- Backend: `backend/OLLAMA_SETUP.md`
- Frontend: Deploy to Vercel, Netlify, or your own server
- Ollama: Consider running on a separate machine for scalability
