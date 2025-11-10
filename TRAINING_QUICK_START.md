# 🚀 Quick Start: Fine-tune Your Code Reviewer

## Option 1: Simple Prompt Tuning (5 minutes, NO TRAINING)

The **fastest** way to improve model performance is to customize the review prompt.

### Edit the review prompt in `backend/src/app.py`:

```python
prompt = f"""You are an expert Python code reviewer specializing in:
1. Finding logical bugs and errors
2. Detecting security vulnerabilities  
3. Suggesting performance improvements
4. Recommending best practices

Analyze the code below and provide:
- Issue severity (CRITICAL, WARNING, SUGGESTION)
- Line number (if applicable)
- Explanation of the issue
- How to fix it

Code:
{req.code}

Static analysis (pylint):
{static_report}

Format your response as a numbered list of issues.
"""
```

Then restart backend:
```bash
cd backend
OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000
```

**No training needed! Works immediately.**

---

## Option 2: Model Parameter Tuning (10 minutes, NO TRAINING)

Adjust model behavior in `backend/src/model.py`:

```python
payload = {
    "model": OLLAMA_MODEL,
    "prompt": prompt,
    "stream": False,
    "temperature": 0.2,    # Lower = more focused (0-1)
    "top_p": 0.85,         # Lower = less random (0-1)
    "top_k": 40,           # Lower = more precise
    "num_predict": 300,    # Max tokens to generate
}
```

**Parameter Guide:**
- `temperature 0.1` = Very focused, deterministic
- `temperature 0.5` = Balanced
- `temperature 0.9` = Creative, more varied

Restart and test. No training needed!

---

## Option 3: Full Fine-tuning (4-8 hours WITH GPU)

Train a custom model on your own data.

### Step 1: Install Training Dependencies

```bash
cd backend

# Option A: Full training (requires GPU)
pip install -r requirements-train.txt

# Option B: Minimal (CPU only, will be slow)
pip install torch transformers datasets peft
```

### Step 2: Prepare Training Data

Use the example `training_data.json` (already provided with 20 examples).

To add more examples, edit `backend/training_data.json`:

```json
[
  {
    "code": "def your_code_here():\n    pass",
    "review": "Your review explaining issues and improvements"
  }
]
```

### Step 3: Run Fine-tuning

```bash
cd backend

# Start training (takes 1-4 hours depending on GPU)
python train.py

# For CPU (very slow, not recommended):
# python train.py
```

### Step 4: Use Fine-tuned Model

```bash
# Option A: Load directly with Ollama (if model format compatible)
# Option B: Export and use with Ollama

# For now, keep using Ollama's base models
```

---

## Recommended Path

### Fast Path (Start Here ⚡)
1. **Customize prompt** (Option 1) - 5 min
2. **Test with different models** (mistral, codellama)
3. **Tune parameters** (Option 2) - 10 min

### Medium Path (Better Results ⭐)
1. Do Fast Path
2. **Create training data** with 50+ code examples
3. **Fine-tune with LoRA** (Option 3) - 2-4 hours with GPU

### Full Path (Best Quality 🏆)
1. Do Medium Path
2. **Collect 500+ real code examples** from your codebase
3. **Full fine-tuning** - 8-24 hours with GPU

---

## Current Setup

You already have:
- ✅ `training_data.json` with 20 examples
- ✅ `train.py` script ready to use
- ✅ `FINE_TUNING.md` with detailed guide
- ✅ `backend/src/app.py` with editable prompt

---

## Next: Try It Now

### Quickest Win (Prompt Tuning)

1. Edit `backend/src/app.py` - customize the prompt
2. Restart backend:
   ```bash
   cd backend
   OLLAMA_MODEL=mistral python -m uvicorn src.app:app --port 8000
   ```
3. Test in browser: http://localhost:5173

### Want to Train?

Ensure you have GPU (check `nvidia-smi` for NVIDIA):

```bash
cd backend
pip install -r requirements-train.txt
python train.py  # Takes 1-4 hours
```

---

## Architecture

```
Raw Code
   ↓
[Your Custom Prompt] ← Edit for quick improvements
   ↓
[Ollama Model] ← Can fine-tune with train.py
   ↓
[AI Review]
   ↓
Frontend Display
```

---

## Tips for Better Results

### Improve Prompt (Fastest ⚡)
```python
# Bad prompt
prompt = "Review this code"

# Good prompt  
prompt = """Review this Python code. Focus on:
1. Logical errors (bugs that cause wrong results)
2. Security issues (SQL injection, hardcoded secrets)
3. Performance problems (O(n²) when O(n) possible)
4. Best practices (use built-ins, avoid eval())

Format: 
- [CRITICAL] if security/data loss
- [WARNING] if major issue
- [SUGGESTION] if improvement

Code: {req.code}"""
```

### Improve Training Data (Most Important 🎯)
- Include 5-10 **real bugs** from your code
- Include 5-10 **best practice fixes**
- Include **different code styles** (short/long functions)
- Include **different domains** (web, ML, CLI, etc)

### Improve Model Selection
```bash
# Fastest (5s)
OLLAMA_MODEL=mistral

# Balanced (15s)
OLLAMA_MODEL=neural-chat

# Best for code (20s)
OLLAMA_MODEL=codellama
```

---

## Troubleshooting

**Training too slow?**
- ✅ Use GPU: `nvidia-smi` should show usage
- ✅ Reduce batch size in `train.py`: `BATCH_SIZE = 2`
- ✅ Use LoRA (already in script)

**Model not improving?**
- ✅ Add more training data (50+ examples)
- ✅ Make examples more specific to your needs
- ✅ Try different model (mistral → codellama)

**Out of memory?**
- ✅ Reduce `BATCH_SIZE` to 1-2
- ✅ Reduce `MAX_SEQ_LENGTH` to 256
- ✅ Use smaller model for fine-tuning

---

## Resources

- `FINE_TUNING.md` - Detailed guide with 3 approaches
- `train.py` - Ready-to-use training script
- `training_data.json` - Example training data (edit to add your own)
- `src/app.py` - Edit prompt here for quick wins

---

**Start with Option 1 (prompt tuning) - it takes 5 minutes and often makes a huge difference!** 🚀
