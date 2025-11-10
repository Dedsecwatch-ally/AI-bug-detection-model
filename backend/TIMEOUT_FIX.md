# Timeout Fix & Optimization Guide

## Issues Fixed

1. ✅ **Frontend timeout increased**: 20s → 120s (2 minutes)
2. ✅ **Backend timeout increased**: 60s → 120s 
3. ✅ **Token reduction**: 800 → 300 tokens (faster responses)
4. ✅ **Better loading message**: Shows wait time estimate

## Why Timeouts Happen

Ollama LLM inference can be slow:
- **First request**: 10-30 seconds (model loads into memory)
- **Subsequent requests**: 5-15 seconds (model stays loaded)
- **Large models** (13B+): Even slower
- **CPU-only systems**: Very slow (use GPU if possible)

## Current Model Performance

You're using **granite3.1-dense** (5GB model):
- ✅ Good quality reviews
- ⏱️ Takes 30-60 seconds per request on typical CPU

## Faster Alternatives

To speed up responses, try these models:

### Option 1: Mistral (FASTEST) ⚡
```bash
# Download
ollama pull mistral

# Run backend with mistral
cd backend
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000
```
- **Speed**: 5-10 seconds per request
- **Quality**: Good (slightly less detailed than Granite)
- **Size**: 4GB

### Option 2: Neural Chat (BALANCED) ⚖️
```bash
ollama pull neural-chat

# Run with neural-chat
OLLAMA_MODEL=neural-chat python -m uvicorn src.app:app --port 8000
```
- **Speed**: 10-15 seconds
- **Quality**: Very good for code
- **Size**: 4GB

### Option 3: CodeLlama (CODE-OPTIMIZED) 🎯
```bash
ollama pull codellama

# Run with codellama
OLLAMA_MODEL=codellama python -m uvicorn src.app:app --port 8000
```
- **Speed**: 15-25 seconds
- **Quality**: Excellent for code reviews
- **Size**: 4GB

## Current Settings (Already Applied)

### Frontend Timeout (`web-ui/src/api.js`)
```javascript
timeout: 120000  // 120 seconds = 2 minutes
```

### Backend Timeout (`backend/src/model.py`)
```python
timeout: 120  # 120 seconds for Ollama API call
```

### Token Limit (`backend/src/app.py`)
```python
max_new_tokens=300  # Reduced from 800 for faster generation
```

## How to Switch Models at Runtime

After downloading a new model with `ollama pull`:

**Option A: Set environment variable**
```bash
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000
```

**Option B: Edit backend/.env (create if needed)**
```bash
OLLAMA_MODEL=mistral
OLLAMA_API_URL=http://localhost:11434
```

## What to Expect

### With Granite3.1-Dense (Current)
- ⏳ First request: 30-60 seconds
- ⏳ Subsequent: 20-30 seconds
- ✅ Quality: Excellent detail

### With Mistral (Recommended for Speed)
- ⏳ First request: 10-15 seconds
- ⏳ Subsequent: 5-10 seconds
- ✅ Quality: Good, sufficient for most code reviews

### With CodeLlama (Best for Code)
- ⏳ First request: 20-30 seconds
- ⏳ Subsequent: 15-20 seconds
- ✅ Quality: Excellent for code-specific issues

## If Still Timing Out

1. **Check Ollama is responsive**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check model is loaded**:
   ```bash
   ollama list  # Should show your model with size
   ```

3. **Check system resources**:
   - Free up RAM (close other apps)
   - Check CPU usage: `top` or Activity Monitor
   - Use smaller model

4. **Increase timeout even more**:
   - Edit `web-ui/src/api.js`: increase `timeout: 180000` (3 minutes)
   - Edit `backend/src/model.py`: increase `timeout=180`

5. **GPU acceleration** (if available):
   - Ollama uses GPU automatically on macOS (Metal)
   - Ensure you have sufficient VRAM
   - Check: `ollama` app settings

## Testing the Fix

After changes, the frontend automatically reloads (Vite HMR). 

**To test**:
1. Go to http://localhost:5173
2. Click "Review Code"
3. Should now wait up to 2 minutes with message: "⏳ Analyzing (may take 30-60 seconds)..."
4. Should complete within 2 minutes

## Recommended Quick Setup

```bash
# Download fastest model
ollama pull mistral

# Terminal 1: Ollama server
ollama serve

# Terminal 2: Backend with mistral
cd backend
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000

# Terminal 3: Frontend
cd web-ui
npx vite
```

This setup should give you:
- ✅ 5-10 second responses
- ✅ Better user experience
- ✅ Good code review quality

---

**Try it now!** The timeouts should be fixed. If you want even faster responses, switch to `mistral` model.
