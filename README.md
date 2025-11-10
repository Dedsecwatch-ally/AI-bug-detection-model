# AI Bug Detection Model

An intelligent code review system that uses fine-tuned language models to detect bugs, code smells, and potential issues in your code. Powered by a locally-trained GPT-2 model with LoRA optimization.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- 🤖 **AI-Powered Code Review**: Uses fine-tuned GPT-2 model to analyze code and suggest improvements
- ⚡ **Local Inference**: Run completely locally without cloud dependencies
- 🎯 **Static Analysis Integration**: Combines AI insights with Pylint for comprehensive code analysis
- 🖥️ **Web UI**: Clean React interface with Monaco Editor for code submission
- 🔧 **VS Code Extension**: Directly review code from your editor
- 📝 **Fine-tuning Capability**: Retrain the model on your own code examples
- 💾 **Efficient Model**: Uses LoRA (Low-Rank Adaptation) for lightweight training (~147K parameters)

## Quick Start (3 Steps)

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node dependencies (for web UI)
cd web-ui
npm install
cd ..
```

### 2. Start the Backend Server

```bash
cd /path/to/ai-bug-finder
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8000
```

The server will start at `http://localhost:8000`

### 3. Start the Web UI

```bash
cd web-ui
npm run dev
```

Open `http://localhost:5173` in your browser and start submitting code for review!

## Project Structure

```
ai-bug-finder/
├── backend/
│   ├── src/
│   │   ├── app.py              # FastAPI server with /review endpoint
│   │   ├── model.py            # Model loading and inference logic
│   │   ├── analysis.py         # Pylint integration for static analysis
│   │   └── utils.py            # Utility functions
│   ├── fine_tuned_model_small/  # Pre-trained GPT-2 model (fine-tuned)
│   ├── training_data.json       # Training examples for the model
│   ├── train_small.py           # Script to retrain model locally
│   └── requirements.txt         # Python dependencies
│
├── web-ui/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── api.js              # API client for backend communication
│   │   ├── main.jsx            # React entry point
│   │   ├── styles.css          # Styling
│   │   └── components/
│   │       └── CodeReviewPanel.jsx  # Review display and patch application
│   ├── package.json
│   └── vite.config.js          # Vite configuration
│
├── vscode-extension/
│   ├── extension.js            # VS Code extension code
│   └── package.json            # Extension metadata
│
├── QUICK_START_LOCAL.md        # Detailed setup guide
└── README.md                    # This file
```

## Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (React UI)     │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────────────────┐
│  FastAPI Backend Server     │
│  (Port 8000)                │
│  - /review endpoint         │
│  - Model inference          │
└────────┬────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌───────────┐
│ GPT-2  │  │  Pylint   │
│ Model  │  │ (Static)  │
└────────┘  └───────────┘
```

## API Endpoints

### POST /review

Submit code for review.

**Request:**
```json
{
  "code": "def foo():\n    x = 10\n    return x"
}
```

**Response:**
```json
{
  "review": "The function looks clean but could benefit from a docstring...",
  "static_report": "Your code: 1 message\n  W0612: unused-variable (line 2)...",
  "patches": ["@@ -1,3 +1,5 @@\n def foo()..."],
  "full_file": "def foo():\n    \"\"\"Return 10.\"\"\"\n    x = 10\n    return x"
}
```

## Configuration

### Model Selection

Set the `BUG_MODEL` environment variable to use a different model:

```bash
# Use the fine-tuned model (default)
export BUG_MODEL="./fine_tuned_model_small"

# Or use Phi-3-mini
export BUG_MODEL="microsoft/phi-3-mini-4k-instruct"

# Then start the server
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8000
```

### Gemini API Integration

For using Google's Gemini model instead:

```bash
export GEMINI_API_KEY="your-api-key"
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8000
```

### Backend Configuration

Edit `backend/src/app.py` to customize:
- Model temperature and max tokens
- Timeout settings
- CORS configuration
- Request validation

### Frontend Configuration

Edit `web-ui/src/api.js` to customize:
- Backend API URL
- Request timeout
- Error handling

## Training Your Own Model

You can fine-tune the model on your own code examples for better results.

### Step 1: Prepare Training Data

Edit `backend/training_data.json` with your code examples:

```json
[
  {
    "code": "def calculate_sum(numbers):\n    total = 0\n    for n in numbers:\n        total += n\n    return total",
    "review": "Function works correctly but could use Python's built-in sum(). Consider: return sum(numbers)"
  },
  ...more examples...
]
```

### Step 2: Run Training

```bash
cd backend
python train_small.py
```

This will:
- Load your training data
- Fine-tune GPT-2 with LoRA (4 rank, ~147K trainable parameters)
- Train for 2 epochs on CPU
- Save to `fine_tuned_model_small/`

### Step 3: Restart Backend

Restart the FastAPI server to use the newly trained model:

```bash
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8000
```

## VS Code Extension

Install and use the extension:

1. Build the extension:
   ```bash
   cd vscode-extension
   npm install
   npm run build
   ```

2. Install in VS Code:
   - Open VS Code
   - Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
   - Search for "AI Bug Finder"
   - Click Install

3. Use it:
   - Open any code file
   - Run command: `Review with AI Bug Finder`
   - View results in the output panel

## Troubleshooting

### Backend server won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>

# Try a different port
PYTHONPATH=$(pwd) python -m uvicorn backend.src.app:app --port 8001
```

### Model loading errors

```bash
# Check if model exists
ls -la backend/fine_tuned_model_small/

# Reinstall dependencies
pip install -r backend/requirements.txt --upgrade

# Use fallback model
export BUG_MODEL="microsoft/phi-3-mini-4k-instruct"
```

### Frontend can't connect to backend

```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check frontend configuration in web-ui/src/api.js
# Make sure API_URL matches your backend address

# Try with explicit backend URL
export VITE_API_URL=http://localhost:8000
npm run dev
```

## Performance

- **Model**: GPT-2 (124M parameters, 548 MB)
- **Training Time**: ~10 seconds for 2 epochs on CPU
- **Inference Time**: ~2-5 seconds per code review
- **Memory Usage**: ~2-3 GB (model + inference)
- **LoRA Training**: Only 147K parameters need to be trained (~0.1% of model)

## Technical Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Server**: Uvicorn
- **ML**: Transformers, PyTorch, PEFT (LoRA)
- **Analysis**: Pylint
- **Dataset**: Hugging Face Datasets

### Frontend
- **Framework**: React 18+
- **Build**: Vite
- **Editor**: Monaco Editor
- **HTTP Client**: Axios

### ML Training
- **Model**: GPT-2 (from Hugging Face)
- **Fine-tuning**: LoRA (Low-Rank Adaptation)
- **Optimization**: Mixed precision, gradient accumulation

## Requirements

- Python 3.10+
- Node.js 16+
- 4GB RAM (8GB+ recommended)
- 2GB disk space for models

## Environment Variables

```bash
# Model configuration
BUG_MODEL=./fine_tuned_model_small
MODEL_MAX_LENGTH=512
MODEL_TEMPERATURE=0.7

# API configuration
GEMINI_API_KEY=your-api-key-here
API_PORT=8000

# Training configuration
TRAINING_EPOCHS=2
TRAINING_BATCH_SIZE=2
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd web-ui
npm test
```

### Linting

```bash
# Python
pylint backend/src/**/*.py

# JavaScript
cd web-ui
npm run lint
```

## Contributing

We welcome contributions! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Improvements

- [ ] Support for multiple programming languages
- [ ] Custom model fine-tuning UI
- [ ] Real-time collaborative code review
- [ ] GitHub integration for automatic PR reviews
- [ ] Larger model options (Mistral, Llama)
- [ ] GPU optimization for faster inference
- [ ] Cloud deployment guides (AWS, Azure, GCP)

## License

MIT License - see LICENSE file for details

## Support

- 📖 [Detailed Setup Guide](./QUICK_START_LOCAL.md)
- 🤖 [Training Guide](./TRAINING_QUICK_START.md)
- 📚 [API Documentation](http://localhost:8000/docs) (when server is running)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Models from [Hugging Face](https://huggingface.co/)
- Code analysis with [Pylint](https://www.pylint.org/)
- UI built with [React](https://react.dev/) and [Vite](https://vitejs.dev/)

---

**Get started now**: Follow the [Quick Start](#quick-start-3-steps) section above!

Have questions? Check out [QUICK_START_LOCAL.md](./QUICK_START_LOCAL.md) for detailed setup instructions.
