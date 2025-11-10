#!/usr/bin/env python3
"""
Lightweight fine-tuning script optimized for local hardware (CPU/small GPU).
Uses DistilBERT (smaller model) with LoRA for efficient code review training.
"""

import json
import os
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    GPT2Tokenizer,
    GPT2LMHeadModel
)
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset

# Configuration - Use MUCH SMALLER model suitable for local hardware
MODEL_ID = "gpt2"  # Small (125M params) - fits in ~500MB
OUTPUT_DIR = "./fine_tuned_model_small"
TRAINING_DATA_FILE = "./training_data.json"

# Training hyperparameters (reduced for smaller model)
LEARNING_RATE = 1e-4
NUM_EPOCHS = 2  # Reduced epochs
BATCH_SIZE = 2  # Very small batch size for CPU/limited GPU
MAX_SEQ_LENGTH = 256  # Shorter sequences
SAVE_STEPS = 5  # Save frequently for safety

def load_training_data(filepath):
    """Load training data from JSON file"""
    if not os.path.exists(filepath):
        print(f"❌ Training data file not found: {filepath}")
        print(f"Create {filepath} with training examples first")
        return None
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Convert to format expected by trainer
    texts = []
    for item in data:
        if isinstance(item, dict) and "text" in item:
            texts.append(item["text"])
        elif isinstance(item, dict) and "code" in item:
            # Convert code/review format to text
            text = f"Code: {item['code']}\nReview: {item['review']}"
            texts.append(text)
    
    return texts

def setup_model(model_id):
    """Load base model and apply LoRA"""
    print(f"📦 Loading model: {model_id}")
    
    # Check device - prefer CPU for stability, can use MPS with limits
    if torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = "cpu"  # Use CPU for MPS to avoid memory issues
    else:
        device = "cpu"
    
    print(f"🖥️  Using device: {device}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with memory optimizations
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32,  # Use full precision for stability
        low_cpu_mem_usage=True
    )
    
    # Configure LoRA with small rank for small model
    print("⚙️  Configuring LoRA...")
    lora_config = LoraConfig(
        r=4,  # Small rank for small model
        lora_alpha=8,
        target_modules=["c_attn"] if "gpt2" in model_id else ["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def prepare_dataset(texts, tokenizer, max_seq_length=256):
    """Prepare dataset for training"""
    print(f"📚 Preparing dataset ({len(texts)} examples)...")
    
    # Create dataset
    dataset = Dataset.from_dict({"text": texts})
    
    # Tokenize with truncation
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=max_seq_length
        )
    
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=["text"],
        batch_size=32
    )
    
    return tokenized_dataset

def train_model(model, tokenizer, dataset, output_dir):
    """Train the model with memory-efficient settings"""
    print(f"🚀 Starting training... (output: {output_dir})")
    print("⚠️  This may take 5-15 minutes on CPU")
    
    # Memory-efficient training config
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        logging_steps=2,
        save_steps=SAVE_STEPS,
        save_total_limit=1,
        report_to="none",
        gradient_accumulation_steps=2,  # Accumulate gradients for effective larger batch
        max_grad_norm=1.0,
        optim="adamw_torch_fused" if torch.cuda.is_available() else "adamw_torch",
        lr_scheduler_type="linear",
        warmup_ratio=0.1
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    # Train
    trainer.train()
    
    # Save fine-tuned model
    print(f"💾 Saving model to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print("✅ Training complete!")
    return model

def main():
    print("=" * 60)
    print("🧠 Code Reviewer Model Fine-tuning (Local/Optimized)")
    print("=" * 60)
    
    # Step 1: Load training data
    print("\n[1/4] Loading training data...")
    texts = load_training_data(TRAINING_DATA_FILE)
    if texts is None:
        return
    print(f"✅ Loaded {len(texts)} training examples")
    
    # Step 2: Setup model with LoRA
    print("\n[2/4] Setting up model...")
    model, tokenizer = setup_model(MODEL_ID)
    print("✅ Model ready")
    
    # Step 3: Prepare dataset
    print("\n[3/4] Preparing dataset...")
    dataset = prepare_dataset(texts, tokenizer, MAX_SEQ_LENGTH)
    print(f"✅ Dataset prepared: {len(dataset)} examples")
    
    # Step 4: Train
    print("\n[4/4] Training model...")
    train_model(model, tokenizer, dataset, OUTPUT_DIR)
    
    print("\n" + "=" * 60)
    print("🎉 Fine-tuning Complete!")
    print("=" * 60)
    print(f"""
✅ Fine-tuned model saved to: {OUTPUT_DIR}

Next steps:

1. **Load the fine-tuned model in your app:**
   
   Edit `backend/src/model.py` and update the model loading:
   
   ```python
   MODEL_NAME = "./fine_tuned_model_small"  # Use fine-tuned model
   tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
   model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
   ```

2. **Restart the backend:**
   
   ```bash
   cd backend
   PYTHONPATH=$(pwd) python -m uvicorn src.app:app --port 8000
   ```

3. **Test the backend with fine-tuned model:**
   
   ```bash
   curl -X POST http://localhost:8000/review \\
     -H "Content-Type: application/json" \\
     -d '{{"code": "def foo():\\n    x = 10\\n    return x"}}'
   ```

4. **For production, use the full model:**
   - When ready, replace with larger model (Mistral, Phi-3, etc.)
   - Use GPU with proper memory management
   - Set up quantization if needed

Note: This fine-tuned model is optimized for your local machine (CPU).
For faster inference, consider GPU acceleration or cloud deployment.
""")

if __name__ == "__main__":
    main()
