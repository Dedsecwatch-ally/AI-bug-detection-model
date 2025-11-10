# Using Ollama 3.2 with AI Bug Finder

This guide explains how to set up and run the AI Bug Finder backend with Ollama for local LLM inference.

## Prerequisites

- **Ollama installed**: Download from [https://ollama.ai](https://ollama.ai)
- **Python 3.8+** with `pip`
- **macOS, Linux, or Windows** (with WSL recommended for Windows)

## Setup Steps

### 1. Install Ollama
Download and install Ollama from https://ollama.ai

### 2. Pull a Model
Run one of these commands to download a model locally:

```bash
# Recommended: Llama 2 (7B, ~4GB)
ollama pull llama2

# Alternative: Mistral (7B, smaller & faster)
ollama pull mistral

# Alternative: Neural Chat (7B, optimized for chat)
ollama pull neural-chat

# Alternative: Llama 2 13B (larger, more capable)
ollama pull llama2:13b
```

### 3. Start Ollama Server
In a terminal, run:

```bash
ollama serve
```

This starts the Ollama API on `http://localhost:11434` (default).

### 4. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 5. Run the Backend
```bash
python -m uvicorn src.app:app --reload --port 8000
```

The API will be available at `http://localhost:8000/docs` (Swagger UI).

## Configuration

### Environment Variables

```bash
# Model to use (default: llama2)
export OLLAMA_MODEL=mistral

# Ollama API endpoint (default: http://localhost:11434)
export OLLAMA_API_URL=http://localhost:11434

# Optional: Custom port for FastAPI
export FASTAPI_PORT=8000
```

## Available Models

Popular lightweight models for code review:

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| Llama 2 7B | ~4GB | Medium | Good | `ollama pull llama2` |
| Mistral 7B | ~4GB | Fast | Good | `ollama pull mistral` |
| Neural Chat 7B | ~4GB | Fast | Good | `ollama pull neural-chat` |
| CodeLlama 7B | ~4GB | Medium | Excellent (code) | `ollama pull codellama` |
| Llama 2 13B | ~8GB | Slow | Excellent | `ollama pull llama2:13b` |

**Recommended for code review**: `codellama` (optimized for programming) or `llama2` (good all-rounder).

## Testing

### Test with curl
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo():\n    return 1"}'
```

### Run unit tests
```bash
cd backend
pytest tests/
```

## Troubleshooting

### Ollama service not available
- Ensure `ollama serve` is running in another terminal
- Check that `http://localhost:11434/api/tags` returns JSON
- Verify firewall isn't blocking port 11434

### Model not found
```bash
# List installed models
ollama list

# Pull a new model
ollama pull llama2
```

### Slow responses
- Use a smaller model: `mistral` or `neural-chat` instead of `llama2:13b`
- Increase `max_new_tokens` in `app.py` (currently 800)
- Check system resources (CPU/RAM/disk)

### Out of memory
- Use a smaller model (see table above)
- Stop other applications
- On macOS: Ollama uses unified memory, no separate VRAM needed

## Production Deployment

For production, consider:

1. **Run Ollama on a separate machine**: Set `OLLAMA_API_URL` to that machine's IP
2. **Use Docker**: Containerize both Ollama and the FastAPI app
3. **Add rate limiting**: Use middleware to prevent abuse
4. **Set timeouts**: Adjust `timeout=60` in `model.py` based on your needs
5. **Monitor resources**: Ollama uses significant CPU/RAM under load

## Stopping Services

```bash
# Stop Ollama (Ctrl+C in its terminal)
# Stop FastAPI (Ctrl+C in its terminal)
```

## Next Steps

- Configure your web-ui to call `http://localhost:8000/review`
- Customize the review prompt in `src/app.py`
- Fine-tune a model with your own training data (advanced)
