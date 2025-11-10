# Local Model Fine-Tuning Guide

This guide shows how to fine-tune Ollama models locally for better code review performance.

## Prerequisites

- **GPU strongly recommended** (fine-tuning on CPU is very slow)
  - NVIDIA GPU: CUDA toolkit installed
  - Apple Silicon: Metal support (automatic)
  - AMD GPU: ROCm support
- **RAM**: 16GB+ recommended
- **Disk space**: 50GB+ for models and datasets
- **Python**: 3.8+

## Two Approaches

### Approach 1: Fine-tune with Ollama (EASIEST) 🎯
Fine-tune using Ollama's built-in capabilities

### Approach 2: Full Fine-tuning with Hugging Face (ADVANCED)
Full control over training parameters using transformers library

## APPROACH 1: Fine-tune with Ollama (RECOMMENDED FOR BEGINNERS)

### Step 1: Create Training Data

Create a file `training_data.jsonl` with your code review examples:

```jsonl
{"prompt": "def foo():\n    x = 10\n    return x", "response": "Issue: Function returns unused variable. Should return a meaningful result."}
{"prompt": "def add(a, b):\n    return a + b", "response": "Good: Simple, clear function with docstring would help. Add: \"\"\"Adds two numbers.\"\"\""}
{"prompt": "x = [1,2,3]\nfor i in range(len(x)):\n    print(x[i])", "response": "Issue: Inefficient loop. Use: for item in x: print(item)"}
```

Save to: `backend/training_data.jsonl`

### Step 2: Prepare Model for Fine-tuning

```bash
cd backend

# Create a modelfile for fine-tuning
cat > Modelfile << 'EOF'
FROM mistral
PARAMETER temperature 0.3
PARAMETER top_p 0.9
EOF
```

### Step 3: Fine-tune the Model

```bash
# Create custom model
ollama create custom-code-reviewer -f Modelfile

# Add training data (Note: Ollama doesn't support direct fine-tuning yet)
# Instead, use the custom model with optimized parameters
```

**Note**: Ollama currently doesn't support direct fine-tuning like Hugging Face. See Approach 2 for full fine-tuning.

---

## APPROACH 2: Full Fine-tuning with Hugging Face Transformers (RECOMMENDED)

This approach gives you full control and better results.

### Step 1: Install Fine-tuning Dependencies

```bash
cd backend

# Activate venv
source venv/bin/activate

# Install training tools
pip install torch transformers datasets peft accelerate wandb
```

### Step 2: Create Training Data

Create `training_data.json`:

```json
[
  {
    "instruction": "Review this Python code for bugs",
    "input": "def foo():\n    x = 10\n    return x",
    "output": "Issue: Unused variable 'x'. The function returns a hard-coded value regardless of the variable."
  },
  {
    "instruction": "Review this Python code for bugs",
    "input": "def add(a, b):\n    return a - b",
    "output": "Critical Bug: Function subtracts instead of adds. Change 'a - b' to 'a + b'"
  },
  {
    "instruction": "Review this Python code for best practices",
    "input": "x = [1,2,3]\nfor i in range(len(x)):\n    print(x[i])",
    "output": "Code smell: Inefficient iteration. Use 'for item in x: print(item)' instead"
  },
  {
    "instruction": "Review this Python code for best practices",
    "input": "def process(data):\n    if data is None:\n        return None\n    return data.strip()",
    "output": "Good: Null check present. Consider adding docstring and handling AttributeError"
  }
]
```

Save to: `backend/training_data.json`

### Step 3: Create Fine-tuning Script

Create `backend/train.py`:

```python
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling
from datasets import Dataset
import os

# Configuration
MODEL_NAME = "mistral-7b"  # or "mistralai/Mistral-7B-v0.1"
OUTPUT_DIR = "./fine_tuned_model"
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
BATCH_SIZE = 4

def load_training_data(filepath):
    """Load JSONL training data"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    formatted_data = []
    for example in data:
        prompt = f"Instruction: {example['instruction']}\nInput: {example['input']}\nOutput: {example['output']}"
        formatted_data.append({"text": prompt})
    
    return formatted_data

def main():
    print("🚀 Starting fine-tuning...")
    
    # Load base model and tokenizer
    print(f"Loading {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Load training data
    print("Loading training data...")
    training_data = load_training_data("training_data.json")
    dataset = Dataset.from_dict({"text": [d["text"] for d in training_data]})
    
    # Tokenize
    print("Tokenizing...")
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=512
        )
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        save_steps=10,
        save_total_limit=2,
        learning_rate=LEARNING_RATE,
        fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
        logging_steps=10,
        report_to="none"  # Disable wandb logging
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    # Fine-tune
    print("⏳ Fine-tuning model... (this may take a while)")
    trainer.train()
    
    # Save model
    print(f"✅ Saving fine-tuned model to {OUTPUT_DIR}")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("✅ Fine-tuning complete!")
    print(f"\nNext steps:")
    print(f"1. Convert model to Ollama format")
    print(f"2. Use: ollama pull llama2")
    print(f"3. Create custom model with fine-tuned weights")

if __name__ == "__main__":
    main()
```

### Step 4: Run Fine-tuning

```bash
cd backend
source venv/bin/activate

# Run training (this takes 30min-2 hours depending on GPU)
python train.py
```

### Step 5: Convert to Ollama Format

After training, convert your model to Ollama:

```bash
# 1. Install ollama tools (if not already)
pip install ollama

# 2. Create Modelfile for your fine-tuned model
cat > Modelfile << 'EOF'
FROM fine_tuned_model  # Your model path
PARAMETER temperature 0.3
PARAMETER top_p 0.9
EOF

# 3. Create custom Ollama model
ollama create my-code-reviewer -f Modelfile

# 4. Use in your app
OLLAMA_MODEL=my-code-reviewer python -m uvicorn src.app:app --port 8000
```

---

## APPROACH 3: Quick LoRA Fine-tuning (FASTEST) ⚡

Use Parameter-Efficient Fine-Tuning (LoRA) for faster, lighter training:

Create `backend/train_lora.py`:

```python
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset
from transformers import DataCollatorForLanguageModeling

MODEL_NAME = "mistralai/Mistral-7B-v0.1"
OUTPUT_DIR = "./lora_model"

def main():
    print("🚀 Starting LoRA fine-tuning...")
    
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    # Wrap model with LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load data and train (same as above)
    # ...
    
    print("✅ LoRA fine-tuning complete!")

if __name__ == "__main__":
    main()
```

**Benefits of LoRA**:
- ✅ 10x faster training
- ✅ 100x smaller model size
- ✅ Lower GPU memory
- ✅ Great results

---

## Minimal Quick Start (No Fine-tuning)

If you just want to **customize the model behavior** without training:

### Option A: System Prompt Tuning

Edit `backend/src/app.py` to customize the review prompt:

```python
prompt = f"""You are an expert Python code reviewer specializing in bug detection and best practices.
Analyze the code for:
1. Logical errors and bugs
2. Performance issues
3. Security vulnerabilities
4. Code style violations
5. Missing error handling

Be concise and provide numbered list of issues.

Code:
{req.code}

Static analysis:
{static_report}

Review:
"""
```

### Option B: Model Parameters Tuning

Edit `backend/src/model.py`:

```python
payload = {
    "model": OLLAMA_MODEL,
    "prompt": prompt,
    "stream": False,
    "temperature": 0.2,  # Lower = more focused, less creative
    "top_p": 0.85,       # Lower = more deterministic
    "top_k": 40,         # Lower = less variety
}
```

---

## Recommended Path

1. **Start**: Option A (System Prompt Tuning) - takes 5 minutes
2. **Then**: Approach 1 (Ollama custom model) - takes 1 hour
3. **Advanced**: Approach 3 (LoRA) - takes 2-4 hours with GPU
4. **Full**: Approach 2 (Full fine-tuning) - takes 4-8 hours with GPU

## Dataset Tips

For best results, create a training dataset with:

- ✅ **Diverse code examples** (simple to complex)
- ✅ **Real bugs** (syntax, logic, performance)
- ✅ **Clear explanations** (what's wrong and why)
- ✅ **Best practices** (refactoring suggestions)
- ✅ **100+ examples minimum** (more is better)

Example format:
```json
{
  "code": "def buggy():\n    for i in range(10):\n        pass",
  "review": "Code smell: Empty loop. Either add functionality or remove."
}
```

## Testing Your Fine-tuned Model

```python
# test_model.py
from transformers import pipeline

model = pipeline("text-generation", model="./fine_tuned_model")
code = "def foo():\n    return 10"
review = model(f"Review this code:\n{code}", max_length=200)
print(review)
```

---

**Ready to train?** Let me know which approach you want to use and I can help you set it up! 🚀
