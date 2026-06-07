#!/usr/bin/env python3
"""
Production-grade QLoRA fine-tuning of Llama 3 8B on the AgroguardAI Agri-QA dataset.

Designed for single-GPU (24 GB VRAM) or multi-GPU (DDP) setups.
Uses 4-bit NF4 quantization, PEFT/LoRA, gradient checkpointing, and
flash-attention-2 for memory efficiency.

Expected training time: ~30-45 min on 1x A100-40GB, ~1.5-2h on 1x A10G-24GB.

Usage:
    python scripts/finetune_llama3.py \
      --model-name meta-llama/Meta-Llama-3-8B \
      --dataset AgroguardAI/agri-qa \
      --output ./models/llama3-agricultural-qlora \
      --batch-size 4 \
      --gradient-accumulation-steps 8 \
      --epochs 3

Requirements:
    pip install transformers accelerate peft bitsandbytes trl datasets
    pip install flash-attn --no-build-isolation  # Recommended but optional

Environment:
    HF_TOKEN must be set for gated model access (Llama 3 requires auth).
    WANDB_API_KEY optional for experiment tracking.
"""

import argparse
import json
import logging
import math
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from accelerate import Accelerator
from accelerate.utils import gather_object
from datasets import Dataset, load_dataset
from peft import (
    LoraConfig,
    PeftModel,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
    TrainerCallback,
    set_seed,
)
from transformers.integrations import WandbCallback

# ── Logging ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Configuration ──────────────────────────────────────────────────────────
@dataclass
class FinetuneConfig:
    """All config in one place — argparse populates this."""

    # Model
    model_name: str = "meta-llama/Meta-Llama-3-8B"
    use_flash_attention: bool = True
    attn_implementation: str = "flash_attention_2"  # auto-set from use_flash_attention

    # Quantization (4-bit NF4)
    load_in_4bit: bool = True
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True

    # LoRA
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: tuple[str, ...] = (
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    )

    # Data
    dataset_name: str = "AgroguardAI/agri-qa"
    max_seq_length: int = 2048
    val_split_ratio: float = 0.10
    num_workers: int = 4

    # Training
    output_dir: str = "./models/llama3-agricultural-qlora"
    num_epochs: int = 3
    per_device_train_batch_size: int = 4
    per_device_eval_batch_size: int = 4
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    weight_decay: float = 0.01
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100
    save_total_limit: int = 3
    fp16: bool = False  # bfloat16 preferred for A100/H100
    bf16: bool = True
    gradient_checkpointing: bool = True
    optim: str = "paged_adamw_8bit"
    seed: int = 42
    report_to: str = "wandb"  # or "none"
    run_name: Optional[str] = None

    # Merge / export
    save_merged: bool = False  # Merge LoRA into base weights for export

    # Resume
    resume_from_checkpoint: Optional[str] = None


# ── Dataset utilities ──────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are AgroguardAI, a trusted agricultural advisory assistant for "
    "smallholder farmers across Sub-Saharan Africa and South Asia. "
    "Provide evidence-based agronomic advice in the farmer's local dialect. "
    "If you lack sufficient information to make a diagnosis, say so clearly "
    "rather than guessing."
)

LLAMA3_CHAT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
    "{system}<|eot_id|>"
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "{question}<|eot_id|>"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "{answer}<|eot_id|>"
)


def format_as_llama3_chat(example: dict) -> dict:
    """Convert a QA pair into Llama 3 chat template format."""
    return {
        "text": LLAMA3_CHAT_TEMPLATE.format(
            system=SYSTEM_PROMPT,
            question=example["question"],
            answer=example["answer"],
        )
    }


def tokenize_function(
    examples: dict,
    tokenizer,
    max_length: int,
) -> dict:
    """Tokenize chat-formatted examples with truncation."""
    result = tokenizer(
        examples["text"],
        truncation=True,
        padding=False,
        max_length=max_length,
        return_tensors=None,
    )
    result["labels"] = result["input_ids"].copy()
    return result


def load_and_prepare_dataset(config: FinetuneConfig, tokenizer) -> tuple[Dataset, Dataset]:
    """Load Agri-QA dataset from Hugging Face Hub, format as chat, tokenize, split."""
    log.info(f"Loading dataset: {config.dataset_name}")

    # Load raw dataset
    ds = load_dataset(config.dataset_name, split="train", data_files="data/agri_qa.json")
    # Note: the HF dataset repo has the raw JSON under data/agri_qa.json

    # Format as Llama 3 chat
    ds = ds.map(format_as_llama3_chat, desc="Formatting as Llama 3 chat")

    # Tokenize
    ds = ds.map(
        lambda x: tokenize_function(x, tokenizer, config.max_seq_length),
        batched=True,
        remove_columns=ds.column_names,
        desc="Tokenizing",
    )

    # Split
    ds = ds.train_test_split(test_size=config.val_split_ratio, seed=config.seed)
    log.info(f"Train: {len(ds['train'])}, Validation: {len(ds['test'])}")
    return ds["train"], ds["test"]


# ── Model setup ────────────────────────────────────────────────────────────
def build_model_and_tokenizer(config: FinetuneConfig):
    """Load quantized base model, tokenizer, apply LoRA."""
    log.info(f"Loading base model: {config.model_name}")

    # Quantization config
    compute_dtype = getattr(torch, config.bnb_4bit_compute_dtype)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config.load_in_4bit,
        bnb_4bit_compute_dtype=config.bnb_4bit_compute_dtype,
        bnb_4bit_quant_type=config.bnb_4bit_quant_type,
        bnb_4bit_use_double_quant=config.bnb_4bit_use_double_quant,
    )

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config.model_name,
        trust_remote_code=False,
        use_fast=True,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Model
    model_kwargs = {
        "quantization_config": bnb_config,
        "device_map": "auto",
        "trust_remote_code": False,
    }
    if config.use_flash_attention:
        model_kwargs["attn_implementation"] = config.attn_implementation

    model = AutoModelForCausalLM.from_pretrained(
        config.model_name,
        **model_kwargs,
    )

    # Prepare for k-bit training
    model = prepare_model_for_kbit_training(
        model,
        use_gradient_checkpointing=config.gradient_checkpointing,
    )

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=list(config.lora_target_modules),
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    return model, tokenizer


# ── Callbacks ──────────────────────────────────────────────────────────────
class PerplexityCallback(TrainerCallback):
    """Compute and log perplexity after each eval."""
    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        if metrics and "eval_loss" in metrics:
            metrics["eval_perplexity"] = math.exp(metrics["eval_loss"])


# ── Main ───────────────────────────────────────────────────────────────────
def parse_args() -> FinetuneConfig:
    parser = argparse.ArgumentParser(
        description="QLoRA fine-tune Llama 3 8B on AgroguardAI Agri-QA"
    )
    # Model
    parser.add_argument("--model-name", default="meta-llama/Meta-Llama-3-8B")
    parser.add_argument("--no-flash-attention", action="store_true",
                        help="Disable flash-attention-2 (fallback to sdpa)")
    # LoRA
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    # Data
    parser.add_argument("--dataset", default="AgroguardAI/agri-qa")
    parser.add_argument("--max-seq-length", type=int, default=2048)
    parser.add_argument("--val-split", type=float, default=0.10)
    # Training
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--warmup-ratio", type=float, default=0.03)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--save-steps", type=int, default=100)
    parser.add_argument("--eval-steps", type=int, default=100)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--bf16", action="store_true", default=True)
    parser.add_argument("--no-bf16", dest="bf16", action="store_false")
    parser.add_argument("--report-to", default="wandb")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--save-merged", action="store_true",
                        help="Merge LoRA into base and save full model")
    parser.add_argument("--resume", default=None, help="Resume from checkpoint")

    args = parser.parse_args()

    cfg = FinetuneConfig()
    cfg.model_name = args.model_name
    cfg.use_flash_attention = not args.no_flash_attention
    cfg.attn_implementation = "flash_attention_2" if cfg.use_flash_attention else "sdpa"
    cfg.lora_r = args.lora_r
    cfg.lora_alpha = args.lora_alpha
    cfg.lora_dropout = args.lora_dropout
    cfg.dataset_name = args.dataset
    cfg.max_seq_length = args.max_seq_length
    cfg.val_split_ratio = args.val_split
    cfg.output_dir = args.output
    cfg.num_epochs = args.epochs
    cfg.per_device_train_batch_size = args.batch_size
    cfg.per_device_eval_batch_size = args.batch_size
    cfg.gradient_accumulation_steps = args.gradient_accumulation_steps
    cfg.learning_rate = args.lr
    cfg.warmup_ratio = args.warmup_ratio
    cfg.seed = args.seed
    cfg.save_steps = args.save_steps
    cfg.eval_steps = args.eval_steps
    cfg.logging_steps = args.logging_steps
    cfg.bf16 = args.bf16
    cfg.report_to = args.report_to
    cfg.run_name = args.run_name
    cfg.save_merged = args.save_merged
    cfg.resume_from_checkpoint = args.resume

    return cfg


def main():
    config = parse_args()
    set_seed(config.seed)

    log.info("=" * 60)
    log.info("AgroguardAI Llama 3 8B QLoRA Fine-Tuning")
    log.info(f"Model: {config.model_name}")
    log.info(f"Dataset: {config.dataset_name}")
    log.info(f"LoRA: r={config.lora_r}, alpha={config.lora_alpha}")
    log.info(f"Training: {config.num_epochs} epochs, "
             f"batch={config.per_device_train_batch_size} x {config.gradient_accumulation_steps} grad-accum, "
             f"lr={config.learning_rate}")
    log.info("=" * 60)

    # Load model & tokenizer
    model, tokenizer = build_model_and_tokenizer(config)

    # Load & prepare data
    train_ds, val_ds = load_and_prepare_dataset(config, tokenizer)

    # Data collator (causal LM — labels = input_ids, no masking needed)
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Training args
    effective_batch = (
        config.per_device_train_batch_size
        * config.gradient_accumulation_steps
        * torch.cuda.device_count()
    )
    total_steps = (
        len(train_ds)
        * config.num_epochs
        // effective_batch
    )

    log.info(f"Effective batch size: {effective_batch}")
    log.info(f"Estimated total steps: {total_steps}")
    log.info(f"GPUs available: {torch.cuda.device_count()}")

    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay,
        warmup_ratio=config.warmup_ratio,
        lr_scheduler_type=config.lr_scheduler_type,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_steps=config.eval_steps,
        evaluation_strategy="steps",
        save_strategy="steps",
        save_total_limit=config.save_total_limit,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        bf16=config.bf16,
        fp16=config.fp16,
        gradient_checkpointing=config.gradient_checkpointing,
        optim=config.optim,
        seed=config.seed,
        report_to=config.report_to if config.report_to != "none" else None,
        run_name=config.run_name or f"llama3-agri-qlora-r{config.lora_r}",
        dataloader_num_workers=config.num_workers,
        logging_dir=os.path.join(config.output_dir, "logs"),
        ddp_find_unused_parameters=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=data_collator,
        callbacks=[PerplexityCallback()],
    )

    # Train
    log.info("Starting training...")
    start = time.time()
    trainer.train(resume_from_checkpoint=config.resume_from_checkpoint)
    elapsed = time.time() - start
    log.info(f"Training completed in {elapsed/60:.1f} minutes")

    # Final evaluation
    eval_results = trainer.evaluate()
    log.info(f"Final eval loss: {eval_results.get('eval_loss', 'N/A'):.4f}")
    if "eval_perplexity" in eval_results:
        log.info(f"Final perplexity: {eval_results['eval_perplexity']:.2f}")

    # Save adapter
    log.info(f"Saving LoRA adapter to {config.output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(config.output_dir)

    # Save training metrics
    metrics_path = os.path.join(config.output_dir, "training_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({
            "train_runtime_seconds": elapsed,
            "eval_loss": eval_results.get("eval_loss"),
            "eval_perplexity": eval_results.get("eval_perplexity"),
            "total_steps": trainer.state.global_step,
            "config": {
                "model_name": config.model_name,
                "lora_r": config.lora_r,
                "lora_alpha": config.lora_alpha,
                "num_epochs": config.num_epochs,
                "learning_rate": config.learning_rate,
                "effective_batch_size": effective_batch,
                "train_samples": len(train_ds),
                "val_samples": len(val_ds),
            }
        }, f, indent=2)
    log.info(f"Metrics saved to {metrics_path}")

    # Optional: merge and save full weights
    if config.save_merged:
        merged_dir = os.path.join(config.output_dir, "merged")
        log.info(f"Merging LoRA into base model → {merged_dir}")
        merged_model = model.merge_and_unload()
        merged_model.save_pretrained(merged_dir)
        tokenizer.save_pretrained(merged_dir)
        log.info("Merged model saved.")

    log.info("Done!")
    log.info(f"Adapter: {config.output_dir}")
    log.info(f"Upload: huggingface-cli upload AgroguardAI/llama3-agri-qlora {config.output_dir}")


if __name__ == "__main__":
    main()
