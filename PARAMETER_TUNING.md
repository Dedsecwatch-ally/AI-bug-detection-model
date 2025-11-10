# Parameter Tuning Guide (Option 2)

## What Are Parameters?

Model parameters control **how** the AI generates responses without changing **what** it looks for.

Think of it like:
- **Prompt** = "What to do" (find bugs, suggest improvements)
- **Parameters** = "How to do it" (be creative, be focused, be brief)

---

## Available Parameters

### 1. **Temperature** (0.0 - 2.0)
Controls randomness/creativity

| Value | Behavior | Best For |
|-------|----------|----------|
| **0.1** | Very focused, deterministic | Consistent bug detection |
| **0.3** | Mostly focused | Reliable reviews |
| **0.5** | Balanced | Default, good quality |
| **0.7** | Somewhat creative | More diverse responses |
| **0.9+** | Very creative, random | Brainstorming |

**Current**: 0.4 (focused)

**Example**:
```
Low (0.1):   Always same answer, very predictable
Mid (0.5):   Mix of consistent & varied
High (0.9):  Different answer each time, less reliable
```

---

### 2. **Top P** (0.0 - 1.0)
Nucleus sampling - keep top N% probable tokens

| Value | Behavior | Best For |
|-------|----------|----------|
| **0.5** | Only most likely words | Very focused |
| **0.8** | Most likely + some variety | Balanced |
| **0.9** | Most likely + good variety | Detailed reviews |
| **0.95** | Most likely + lots of options | Creative |

**Current**: 0.9 (inclusive)

**Example**:
```
Low (0.5):   Only obvious words
Mid (0.8):   Good mix
High (0.95): Considers many options
```

---

### 3. **Top K** (0+)
Keep top K most likely tokens

| Value | Behavior | Best For |
|-------|----------|----------|
| **10** | Very focused, only best options | Precise |
| **40** | Good balance | Most use cases |
| **100** | More variety | Diverse output |
| **0** | No limit | Creative |

**Current**: 40 (balanced)

**Example**:
```
Low (10):    "The answer is definitely X"
Mid (40):    "X is good, Y could work too"
High (100):  "Many options are possible"
```

---

### 4. **Num Predict** (1+)
Maximum number of tokens to generate

| Value | Behavior | Best For |
|-------|----------|----------|
| **100** | Short answers, ~50 words | Quick feedback |
| **300** | Medium answers, ~150 words | Balanced reviews |
| **500** | Detailed answers, ~250 words | In-depth analysis |
| **1000** | Very long, ~500 words | Comprehensive |

**Current**: 300 (medium)

**Example**:
```
100:   "Use 'for x in list' instead of range(len)"
300:   "Use 'for x in list' instead of range(len). This is more Pythonic..."
500:   "Use 'for x in list' instead of range(len). This is more Pythonic and readable because..."
```

---

### 5. **Repeat Penalty** (1.0+)
Penalizes repeating the same words

| Value | Behavior | Best For |
|-------|----------|----------|
| **1.0** | No penalty | Natural text |
| **1.1** | Slight penalty | Avoid repetition |
| **1.5** | Strong penalty | Diverse vocabulary |
| **2.0** | Very strong | Force variety |

**Current**: 1.1 (slight)

**Example**:
```
1.0:  "This is bad, this is bad, this is bad"
1.1:  "This is bad, it's problematic, very problematic"
1.5:  "This is bad, problematic, concerning"
```

---

## Quick Presets

### 🎯 Focused & Precise
Best for: Consistent bug detection
```bash
OLLAMA_TEMPERATURE=0.2 \
OLLAMA_TOP_P=0.8 \
OLLAMA_TOP_K=20 \
OLLAMA_NUM_PREDICT=300 \
OLLAMA_REPEAT_PENALTY=1.2 \
python -m uvicorn src.app:app --port 8000
```

### ⚖️ Balanced (Default)
Best for: Good quality, reasonable responses
```bash
OLLAMA_TEMPERATURE=0.4 \
OLLAMA_TOP_P=0.9 \
OLLAMA_TOP_K=40 \
OLLAMA_NUM_PREDICT=300 \
python -m uvicorn src.app:app --port 8000
```

### 🎨 Creative & Detailed
Best for: Diverse, thorough reviews
```bash
OLLAMA_TEMPERATURE=0.7 \
OLLAMA_TOP_P=0.95 \
OLLAMA_TOP_K=50 \
OLLAMA_NUM_PREDICT=500 \
python -m uvicorn src.app:app --port 8000
```

### ⚡ Quick & Short
Best for: Fast feedback, concise answers
```bash
OLLAMA_TEMPERATURE=0.3 \
OLLAMA_TOP_P=0.85 \
OLLAMA_TOP_K=30 \
OLLAMA_NUM_PREDICT=150 \
python -m uvicorn src.app:app --port 8000
```

---

## How to Use

### Method 1: Command Line (Fastest)
```bash
cd backend

# Set parameters and run
OLLAMA_TEMPERATURE=0.3 \
OLLAMA_TOP_P=0.85 \
OLLAMA_TOP_K=30 \
python -m uvicorn src.app:app --port 8000
```

### Method 2: .env File (Recommended)
Create `backend/.env`:
```
OLLAMA_TEMPERATURE=0.3
OLLAMA_TOP_P=0.85
OLLAMA_TOP_K=30
OLLAMA_NUM_PREDICT=300
OLLAMA_REPEAT_PENALTY=1.1
```

Then restart backend (it will read from .env).

### Method 3: Edit Code (Permanent)
Edit `backend/src/model.py`:
```python
TEMPERATURE = 0.3      # Change default here
TOP_P = 0.85           # Change default here
# etc.
```

---

## Experimentation Guide

### Quick Testing Steps

1. **Start with balanced preset**
   ```bash
   # Run balanced version
   cd backend
   OLLAMA_TEMPERATURE=0.4 OLLAMA_TOP_P=0.9 \
   python -m uvicorn src.app:app --port 8000
   ```

2. **Test with sample code**
   - Go to http://localhost:5173
   - Paste some code
   - Click "Review Code"

3. **Adjust one parameter**
   - Stop server (Ctrl+C)
   - Change ONE parameter
   - Restart and test
   - Compare results

4. **Iterate**
   - Keep good changes
   - Adjust next parameter

### Sample Test Code

```python
# Paste this in browser to test
def foo():
    x = 10
    y = 20
    return x  # Bug: should return x + y
```

With different parameters, you should see:
- **Low temperature**: "This is a bug, fix it"
- **High temperature**: "This has issues. The variable y is unused. The function should probably return..."

---

## Common Adjustments

### Problem: Responses Too Short
**Solution**: Increase `NUM_PREDICT`
```bash
OLLAMA_NUM_PREDICT=500  # Was 300
```

### Problem: Responses Too Long
**Solution**: Decrease `NUM_PREDICT`
```bash
OLLAMA_NUM_PREDICT=150  # Was 300
```

### Problem: Inconsistent Results
**Solution**: Lower `TEMPERATURE`
```bash
OLLAMA_TEMPERATURE=0.2  # Was 0.4
```

### Problem: Bland, Repetitive
**Solution**: Increase `TOP_P` and `TOP_K`
```bash
OLLAMA_TOP_P=0.95       # Was 0.9
OLLAMA_TOP_K=60         # Was 40
```

### Problem: Too Creative/Irrelevant
**Solution**: Lower `TEMPERATURE` and `TOP_P`
```bash
OLLAMA_TEMPERATURE=0.2  # Was 0.4
OLLAMA_TOP_P=0.8        # Was 0.9
```

---

## Parameter Interaction

Parameters work together:

```
High Temperature + High Top P = Very random
High Temperature + Low Top P = Somewhat random
Low Temperature + High Top P = Focused but varied
Low Temperature + Low Top P = Consistent and precise
```

**Recommended approach**: Adjust `TEMPERATURE` first, then `TOP_P`, then others.

---

## Restart Commands

After changing parameters in command line:

```bash
# Stop current server (Ctrl+C)

# Start with new parameters
cd backend
OLLAMA_TEMPERATURE=YOUR_VALUE \
python -m uvicorn src.app:app --port 8000
```

Or use `.env` file (auto-reload when you restart).

---

## Performance Impact

- ✅ **Temperature**: No impact on speed
- ✅ **Top P/K**: Minor impact (10-15% slower with high values)
- ⚠️ **Num Predict**: Significant impact (longer responses = slower)
- ✅ **Repeat Penalty**: No impact on speed

**If too slow**: Reduce `NUM_PREDICT` from 300 to 200.

---

## Parameter Tuning Checklist

- [ ] Read this guide
- [ ] Try balanced preset (default settings)
- [ ] Test with sample code
- [ ] Adjust temperature (control randomness)
- [ ] Adjust top_p (control variety)
- [ ] Adjust num_predict (control length)
- [ ] Find your sweet spot
- [ ] Save in .env file

---

## Current Defaults (Already Optimized)

```
TEMPERATURE = 0.4       ← Focused but not rigid
TOP_P = 0.9             ← Good variety
TOP_K = 40              ← Balanced options
NUM_PREDICT = 300       ← Good length (not too short/long)
REPEAT_PENALTY = 1.1    ← Slight variety
```

These are already tuned for code review. Good starting point!

---

## Next Steps

1. **Try the default** (already good!)
2. **Test different presets** (see "Quick Presets" above)
3. **Adjust one parameter** at a time
4. **Save your best settings** to `.env`

Good luck! 🎯
