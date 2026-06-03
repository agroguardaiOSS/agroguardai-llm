"""
Fine-tune a base LLM (Mistral-7B or TinyLlama) with QLoRA / LoRA.

Loads config from config/lora_config.yaml, processes the Agri-QA dataset,
trains a LoRA adapter, saves it locally, and optionally pushes to Hub.

Usage:
    python src/train.py                          # uses config/lora_config.yaml
    python src/train.py --config my_config.yaml  # custom config
"""

import argparse
import json
import os
from pathlib import Path

import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


def load_config(path: str) -> dict:
    """Load and validate the YAML config."""
    with open(path) as f:
        cfg = yaml.safe_load(f)
    required = ("model", "quantization", "lora", "training", "output")
    missing = [k for k in required if k not in cfg]
    if missing:
        raise KeyError(f"Missing config sections: {missing}")
    return cfg


def build_model_and_tokenizer(cfg: dict):
    """Load base model + tokenizer with optional 4-bit quantization."""
    model_id = cfg["model"]["base_model"]
    tokenizer_id = cfg["model"]["tokenizer"] or model_id
    max_seq_length = cfg["model"].get("max_seq_length", 2048)

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
    tokenizer.pad_token = tokenizer.eos_token or tokenizer.pad_token
    tokenizer.model_max_length = max_seq_length

    quant_cfg = cfg["quantization"]
    if quant_cfg.get("load_in_4bit", True):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=getattr(torch, quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16")),
            bnb_4bit_quant_type=quant_cfg.get("bnb_4bit_quant_type", "nf4"),
            bnb_4bit_use_double_quant=quant_cfg.get("bnb_4bit_use_double_quant", True),
        )
    else:
        bnb_config = None

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if quant_cfg.get("bnb_4bit_compute_dtype", "bfloat16") == "bfloat16" else torch.float16,
    )

    # Prepare model for k-bit training (QLoRA)
    if bnb_config is not None:
        model = prepare_model_for_kbit_training(model)

    # Wrap with LoRA
    lora_cfg = cfg["lora"]
    peft_config = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["alpha"],
        lora_dropout=lora_cfg["dropout"],
        target_modules=lora_cfg["target_modules"],
        task_type=getattr(TaskType, lora_cfg.get("task_type", "CAUSAL_LM")),
        bias="none",
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    return model, tokenizer, peft_config


def tokenize_function(examples, tokenizer, max_seq_length: int):
    """Tokenize text field with truncation and padding."""
    result = tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=max_seq_length,
    )
    # Labels = input_ids for causal LM
    result["labels"] = result["input_ids"].copy()
    return result


def main():
    parser = argparse.ArgumentParser(description="Fine-tune AgroguardAI-LLM")
    parser.add_argument("--config", default="config/lora_config.yaml", help="Path to LoRA config YAML")
    parser.add_argument("--data", default="data/processed/", help="Path to tokenized dataset directory")
    args = parser.parse_args()

    cfg = load_config(args.config)

    print("=" * 60)
    print(f"Base model: {cfg['model']['base_model']}")
    print(f"LoRA rank: {cfg['lora']['r']}, alpha: {cfg['lora']['alpha']}")
    print(f"4-bit quantization: {cfg['quantization']['load_in_4bit']}")
    print("=" * 60)

    model, tokenizer, peft_config = build_model_and_tokenizer(cfg)

    # Load dataset
    data_dir = args.data
    dataset = load_dataset("json", data_files={
        "train": f"{data_dir}/train.jsonl",
        "validation": f"{data_dir}/validation.jsonl",
    })

    max_seq_length = cfg["model"].get("max_seq_length", 2048)
    tokenized = dataset.map(
        lambda x: tokenize_function(x, tokenizer, max_seq_length),
        batched=True,
        remove_columns=dataset["train"].column_names,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    train_cfg = cfg["training"]
    training_args = TrainingArguments(
        output_dir=cfg["output"]["adapter_dir"],
        per_device_train_batch_size=train_cfg.get("per_device_train_batch_size", 2),
        gradient_accumulation_steps=train_cfg.get("gradient_accumulation_steps", 4),
        num_train_epochs=train_cfg.get("num_train_epochs", 3),
        learning_rate=train_cfg.get("learning_rate", 2e-4),
        lr_scheduler_type=train_cfg.get("lr_scheduler_type", "cosine"),
        warmup_ratio=train_cfg.get("warmup_ratio", 0.03),
        weight_decay=train_cfg.get("weight_decay", 0.01),
        logging_steps=train_cfg.get("logging_steps", 10),
        save_steps=train_cfg.get("save_steps", 100),
        eval_steps=train_cfg.get("eval_steps", 100),
        max_grad_norm=train_cfg.get("max_grad_norm", 0.3),
        fp16=train_cfg.get("fp16", False),
        bf16=train_cfg.get("bf16", True),
        optim=train_cfg.get("optim", "paged_adamw_8bit"),
        gradient_checkpointing=train_cfg.get("gradient_checkpointing", True),
        evaluation_strategy="steps",
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        run_name="agroguardai-llm-lora",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    print("\nStarting training...\n")
    trainer.train()

    # Save final adapter
    adapter_dir = cfg["output"]["adapter_dir"]
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    print(f"\n[✓] Adapter saved to {adapter_dir}")

    # Push to Hub if configured
    hub_id = cfg["output"].get("hub_model_id", "")
    if hub_id:
        model.push_to_hub(hub_id)
        tokenizer.push_to_hub(hub_id)
        print(f"[✓] Pushed to Hugging Face Hub: {hub_id}")


if __name__ == "__main__":
    main()
