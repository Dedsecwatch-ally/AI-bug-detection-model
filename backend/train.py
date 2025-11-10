#!/usr/bin/env python3
"""
Simple fine-tuning script for code review model.
Uses LoRA for efficient parameter tuning.
"""

import json
import os
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset

# Configuration
MODEL_ID = "mistralai/Mistral-7B-v0.1"  # Base model
OUTPUT_DIR = "./fine_tuned_model"
TRAINING_DATA_FILE = "./training_data.json"

# Training hyperparameters
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
BATCH_SIZE = 4
MAX_SEQ_LENGTH = 512

def load_training_data(filepath):
    """Load training data from JSON file"""
    if not os.path.exists(filepath):
        print(f"❌ Training data file not found: {filepath}")
        print(f"Create {filepath} with training examples first")
        print("Example format:")
        print("""[
  {
    "text": "Code: def foo():\\n    x = 10\\nReview: Remove unused variable x"
  }
]""")
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
    
    # Check GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Using device: {device}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto" if device == "cuda" else None,
        load_in_8bit=device == "cuda"  # 8-bit quantization for GPU efficiency
    )
    
    # Configure LoRA
    print("⚙️  Configuring LoRA...")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj", "k_proj", "out_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer

def prepare_dataset(texts, tokenizer, max_seq_length=512):
    """Prepare dataset for training"""
    print(f"📚 Preparing dataset ({len(texts)} examples)...")
    
    # Create dataset
    dataset = Dataset.from_dict({"text": texts})
    
    # Tokenize
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
        remove_columns=["text"]
    )
    
    return tokenized_dataset

def train_model(model, tokenizer, dataset, output_dir):
    """Train the model"""
    print(f"🚀 Starting training... (output: {output_dir})")
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        save_steps=50,
        save_total_limit=2,
        learning_rate=LEARNING_RATE,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
        logging_dir="./logs",
        report_to="none"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    
    trainer.train()
    
    # Save fine-tuned model
    print(f"💾 Saving model to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print("✅ Training complete!")
    return model

def main():
    print("=" * 60)
    print("🧠 Code Reviewer Model Fine-tuning")
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
Next steps:

1. Model saved to the `./fine_tuned_model` directory above.

2. To use the fine-tuned model locally, update your inference code to point
    at the saved model path and load it via `transformers`:

    ```python
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
    model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")
    ```

3. Restart the backend and ensure `backend/src/model.py` loads your fine-tuned
    model path when configured.
""")

if __name__ == "__main__":
    main()
