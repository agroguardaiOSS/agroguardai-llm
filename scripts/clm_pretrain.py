#!/usr/bin/env python3
"""
Continued pre-training (CLM) on Agricultural Corpus — Raw PyTorch loop.
Uses TinyLlama 1.1B with LoRA, CPU-only. Avoids HuggingFace Dataset (Py3.14 compat).

Strategy:
- TinyLlama/TinyLlama-1.1B-Chat-v1.0 as base
- LoRA rank=8 (~0.1% trainable params)
- FP32 on CPU
- Gradient checkpointing
- Batch size 1, gradient accumulation 4 → effective batch 4
- Target: 200 steps
"""

import sys
import torch
import json
import math
from pathlib import Path
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model, TaskType

def log(msg):
    print(msg, flush=True)

# ── Config ────────────────────────────────────────────────────────────────
BASE_MODEL = "gpt2"
DATA_DIR = Path("/home/nebula/agroguardai-llm/data/processed")
OUTPUT_DIR = Path("/home/nebula/agroguardai-llm/models/clm-checkpoint")
MAX_LENGTH = 128
BATCH_SIZE = 1
GRADIENT_ACCUMULATION = 4
LEARNING_RATE = 5e-5
MAX_STEPS = 50
WARMUP_STEPS = 5
LOGGING_STEPS = 5
EVAL_STEPS = 25
SEED = 42

torch.manual_seed(SEED)

# ── Simple dataset (no HF Dataset dependency) ─────────────────────────────
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoded = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt",
        )
        input_ids = encoded["input_ids"].squeeze(0)
        attention_mask = encoded["attention_mask"].squeeze(0)
        # For CLM, labels = input_ids (shifted internally by model)
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": input_ids.clone(),
        }

# ── Load tokenizer ────────────────────────────────────────────────────────
log("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# ── Load data ─────────────────────────────────────────────────────────────
def load_jsonl(path):
    samples = []
    with open(path) as f:
        for line in f:
            samples.append(json.loads(line))
    return samples

log("Loading training data...")
train_raw = load_jsonl(DATA_DIR / "train.jsonl")
val_raw = load_jsonl(DATA_DIR / "validation.jsonl")
train_texts = [s["text"] for s in train_raw]
val_texts = [s["text"] for s in val_raw]
log(f"  Train samples: {len(train_texts)}")
log(f"  Val samples:   {len(val_texts)}")

train_dataset = TextDataset(train_texts, tokenizer, MAX_LENGTH)
val_dataset = TextDataset(val_texts, tokenizer, MAX_LENGTH)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False, num_workers=0)

# ── Load model ────────────────────────────────────────────────────────────
log(f"Loading base model: {BASE_MODEL}")
log("  (CPU-only — downloading ~2.2GB, may take a moment...)")

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float32,
    device_map=None,
    low_cpu_mem_usage=True,
)
# No gradient checkpointing needed for 124M model on CPU

# ── Apply LoRA ────────────────────────────────────────────────────────────
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=4,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["c_attn", "c_proj"],
    bias="none",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ── Optimizer & scheduler ─────────────────────────────────────────────────
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=WARMUP_STEPS,
    num_training_steps=MAX_STEPS,
)

# ── Training loop ─────────────────────────────────────────────────────────
log(f"\nStarting CLM continued pre-training...")
log(f"  Max steps: {MAX_STEPS}")
log(f"  Effective batch: {BATCH_SIZE * GRADIENT_ACCUMULATION}")
log(f"  Learning rate: {LEARNING_RATE}\n")

model.train()
global_step = 0
accum_loss = 0.0
train_iter = iter(train_loader)

while global_step < MAX_STEPS:
    # Accumulate gradients
    accum_loss = 0.0
    for micro_step in range(GRADIENT_ACCUMULATION):
        try:
            batch = next(train_iter)
        except StopIteration:
            train_iter = iter(train_loader)
            batch = next(train_iter)

        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        labels = batch["labels"]

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )
        loss = outputs.loss / GRADIENT_ACCUMULATION
        loss.backward()
        accum_loss += loss.item()

    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    scheduler.step()
    optimizer.zero_grad()
    global_step += 1

    if global_step % LOGGING_STEPS == 0:
        lr = scheduler.get_last_lr()[0]
        log(f"  Step {global_step:4d}/{MAX_STEPS} | loss={accum_loss:.4f} | lr={lr:.2e}")

    # Evaluation
    if global_step % EVAL_STEPS == 0:
        model.eval()
        val_loss = 0.0
        val_count = 0
        with torch.no_grad():
            for val_batch in val_loader:
                v_outputs = model(
                    input_ids=val_batch["input_ids"],
                    attention_mask=val_batch["attention_mask"],
                    labels=val_batch["labels"],
                )
                val_loss += v_outputs.loss.item()
                val_count += 1
        avg_val_loss = val_loss / max(val_count, 1)
        ppl = math.exp(avg_val_loss)
        log(f"  >>> Eval  @ step {global_step}: loss={avg_val_loss:.4f}  perplexity={ppl:.2f}")
        model.train()

# ── Save adapter ──────────────────────────────────────────────────────────
log("\nSaving LoRA adapter...")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
model.save_pretrained(str(OUTPUT_DIR))
tokenizer.save_pretrained(str(OUTPUT_DIR))
log(f"  Adapter saved to: {OUTPUT_DIR}")

# ── Final eval ────────────────────────────────────────────────────────────
model.eval()
val_loss = 0.0
val_count = 0
with torch.no_grad():
    for val_batch in val_loader:
        v_outputs = model(
            input_ids=val_batch["input_ids"],
            attention_mask=val_batch["attention_mask"],
            labels=val_batch["labels"],
        )
        val_loss += v_outputs.loss.item()
        val_count += 1
avg_val_loss = val_loss / max(val_count, 1)
ppl = math.exp(avg_val_loss)

log(f"\n{'='*55}")
log(f"  Continued Pre-Training Complete")
log(f"{'='*55}")
log(f"  Steps trained:    {MAX_STEPS}")
log(f"  Eval loss:        {avg_val_loss:.4f}")
log(f"  Eval perplexity:  {ppl:.2f}")
log(f"  Adapter:          {OUTPUT_DIR}")
log(f"{'='*55}")
