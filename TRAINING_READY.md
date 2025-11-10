# Model Training Setup Complete ✅

You now have everything needed to train your code reviewer model locally!

## Files Created

### 📚 Documentation
- **`TRAINING_QUICK_START.md`** ⭐ START HERE - Quick guide with 3 options
- **`FINE_TUNING.md`** - Detailed guide with multiple approaches
- **`TIMEOUT_FIX.md`** - How to fix timeout issues

### 🔧 Code & Data
- **`train.py`** - Ready-to-use fine-tuning script (LoRA method)
- **`training_data.json`** - Example training data (20 code reviews)
- **`requirements-train.txt`** - Dependencies for training

## Three Training Options

### Option 1: Prompt Tuning (5 minutes) ⚡ RECOMMENDED
- Edit the review prompt in `backend/src/app.py`
- No training required, immediate results
- Great for customizing to your use case
- **Best for**: Getting started quickly

### Option 2: Parameter Tuning (10 minutes) 
- Adjust temperature, top_p, token limits
- Controls model behavior without training
- Fast to experiment with
- **Best for**: Fine-tuning existing models

### Option 3: Full Fine-tuning (2-8 hours) 🏆
- Train model on your own code examples
- Requires GPU (NVIDIA/Apple Silicon/AMD)
- Best results but most time-consuming
- Uses LoRA for efficient training
- **Best for**: Production deployment

## Quick Start

### Try Prompt Tuning First (5 min)

```bash
# 1. Edit the prompt
nano backend/src/app.py
# Find and customize the prompt variable

# 2. Restart backend
cd backend
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000

# 3. Test in browser
# http://localhost:5173
```

### Want to Fine-tune? (4-8 hours)

```bash
# 1. Install training dependencies
cd backend
pip install torch transformers datasets peft

# 2. Optionally add more training examples
# Edit training_data.json

# 3. Start training
python train.py

# Training progress will show, takes 1-4 hours with GPU
```

## What's Included

### Training Data
- **20 code examples** covering:
  - Bugs (logic, syntax, security)
  - Best practices
  - Performance issues
  - Pythonic patterns

### Training Script (`train.py`)
- Loads training data from JSON
- Sets up model with LoRA (efficient)
- Handles GPU/CPU automatically
- Saves fine-tuned weights
- Shows progress and statistics

### Documentation
- **TRAINING_QUICK_START.md** - Simple 3-option guide
- **FINE_TUNING.md** - Deep dive with 3 approaches
- **TIMEOUT_FIX.md** - Performance optimization

## System Requirements

### For Prompt/Parameter Tuning
- ✅ Any computer (no GPU needed)
- ✅ Just CPU
- ✅ 5-10 minutes total

### For Fine-tuning
- ✅ **GPU strongly recommended**
  - NVIDIA: CUDA 11.8+ (RTX 3060 minimum)
  - Apple Silicon: Automatic (M1/M2/M3)
  - AMD: ROCm support

- ⚠️ **Possible on CPU** but slow:
  - 4+ hours instead of 1 hour
  - Not recommended for first run

- 💾 **Disk**: 50GB+ for models
- 🧠 **RAM**: 16GB+ recommended

## Recommended Approach

```
Start
  ↓
[Option 1: Prompt Tuning] ← Do this first (5 min)
  ↓ Not satisfied?
[Option 2: Parameter Tuning] ← Adjust model (10 min)
  ↓ Still want more?
[Option 3: Fine-tuning] ← Full training (4-8 hours)
```

## Expected Results

### After Prompt Tuning
- ✅ More focused reviews
- ✅ Better format control
- ✅ Domain-specific guidance
- ⏱️ No model update needed

### After Fine-tuning
- ✅ Better understanding of your code patterns
- ✅ More accurate issue detection
- ✅ Customized explanations
- ⏱️ Same response time as base model

## Next Steps

1. **Read**: `TRAINING_QUICK_START.md` (5 min read)
2. **Try**: Option 1 (Prompt Tuning) (5 min)
3. **Evaluate**: See if results improved
4. **Decide**: Try Option 2 or 3 if needed

## File Locations

```
backend/
├── train.py                    # Training script
├── training_data.json          # Training examples (edit to add yours)
├── requirements-train.txt      # Training dependencies
├── fine_tuned_model/           # Output dir (created after training)
└── src/
    └── app.py                  # Edit the prompt here!

/
├── TRAINING_QUICK_START.md    # ⭐ Start here
├── FINE_TUNING.md             # Detailed guide
└── TIMEOUT_FIX.md             # Performance help
```

## Helpful Commands

```bash
# Check GPU availability
nvidia-smi  # NVIDIA
python -c "import torch; print(torch.cuda.is_available())"

# Install training packages
pip install -r backend/requirements-train.txt

# Run training
cd backend && python train.py

# List current models
ollama list

# Switch model
OLLAMA_MODEL=codellama python -m uvicorn src.app:app --port 8000
```

## Support

For detailed information, see:
- **Quick questions**: Read TRAINING_QUICK_START.md
- **Implementation details**: Read FINE_TUNING.md
- **Performance issues**: Read TIMEOUT_FIX.md
- **Code**: Check train.py with comments

---

## What to Do Now

### 🎯 Recommendation
Start with **Option 1: Prompt Tuning** (TRAINING_QUICK_START.md)
- Takes only 5 minutes
- Often gives great results
- No GPU needed
- Easy to experiment

Then, if you want even better results, move to fine-tuning.

**Let's train!** 🚀
