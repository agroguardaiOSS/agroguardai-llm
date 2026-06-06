#!/usr/bin/env python3
"""
Fine-tune AgroGuardAI-LLM with QLoRA.
Trains on data/processed/train_split.json, validates on data/processed/val_split.json.
Saves the best checkpoint based on validation loss.

Usage:
    python scripts/fine_tune.py
"""

import json
import os
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

BASE_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
TRAIN_DATA = "data/processed/train_split.json"
VAL_DATA = "data/processed/val_split.json"
OUTPUT_DIR = "models/agroguardai-fine-tune"


def format_example(example: dict) -> str:
    """Convert a raw agro-QA record into the chat-formatted text string."""
    region = example.get("region", "Nigeria")
    dialect = example.get("dialect", "English")
    crop = example.get("crop", "crops")

    system_msg = (
        "You are AgroguardAI, an agricultural assistant for smallholder farmers. "
        "You provide safe, evidence-based advice. When you lack information, you refuse to guess. "
        "You match the farmer's dialect and never recommend banned or dangerous products. "
        "Always cite your sources."
    )

    user_msg = (
        f"A farmer asks the following question in {dialect} about {crop} in {region}. "
        f"Respond with safe, practical agronomic advice in the same dialect.\n\n"
        f"Farmer: {example['question']}"
    )

    assistant_msg = example["answer"]

    text = (
        f"<|system|>\n{system_msg}</s>\n"
        f"<|user|>\n{user_msg}</s>\n"
        f"<|assistant|>\n{assistant_msg}</s>\n"
    )
    return text


def load_and_format(path: str) -> Dataset:
    """Load a JSON list of records and format each into a `text` field."""
    with open(path) as f:
        records = json.load(f)

    formatted = [{"text": format_example(r)} for r in records]
    return Dataset.from_list(formatted)


def main():
    print("=" * 60)
    print("AgroGuardAI-LLM — Fine-Tuning Script")
    print(f"Base model: {BASE_MODEL}")
    print("LoRA: r=32, alpha=64 | Epochs: 2 | QLoRA (4-bit)")
    print("=" * 60)

    # ── Load datasets ──────────────────────────────────────────────
    print("\n[1/5] Loading datasets...")
    train_dataset = load_and_format(TRAIN_DATA)
    val_dataset = load_and_format(VAL_DATA)
    print(f"  Train: {len(train_dataset)} examples")
    print(f"  Val:   {len(val_dataset)} examples")

    # ── Tokeniser ──────────────────────────────────────────────────
    print("\n[2/5] Loading tokeniser...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token or tokenizer.pad_token
    tokenizer.model_max_length = 2048

    def tokenize_function(examples):
        result = tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=2048,
        )
        result["labels"] = result["input_ids"].copy()
        return result

    tokenized_train = train_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    tokenized_val = val_dataset.map(tokenize_function, batched=True, remove_columns=["text"])

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # ── Model with QLoRA ──────────────────────────────────────────
    print("\n[3/5] Loading model with 4-bit QLoRA...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )

    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        target_modules=["all-linear"],
        task_type=TaskType.CAUSAL_LM,
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── Training arguments ────────────────────────────────────────
    print("\n[4/5] Configuring trainer...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        num_train_epochs=2,
        learning_rate=2.0e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        weight_decay=0.01,
        logging_steps=10,
        save_steps=100,
        eval_steps=100,
        max_grad_norm=0.3,
        fp16=False,
        bf16=True,
        optim="paged_adamw_8bit",
        gradient_checkpointing=True,
        evaluation_strategy="steps",
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        run_name="agroguardai-llm-lora",
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    # ── Train ──────────────────────────────────────────────────────
    print("\n[5/5] Starting training...\n")
    trainer.train()

    # Save final adapter
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"\n[OK] Final adapter saved to {OUTPUT_DIR}")

    # Print best checkpoint info
    if trainer.state.best_model_checkpoint:
        print(f"[OK] Best checkpoint (eval_loss={trainer.state.best_metric:.4f}): {trainer.state.best_model_checkpoint}")


if __name__ == "__main__":
    main()
