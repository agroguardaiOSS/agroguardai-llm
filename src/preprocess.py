"""
Format and tokenize the Agri-QA dataset for Hugging Face fine-tuning.

Input:  data/agri_qa.json  (list of {id, region, dialect, crop, question, answer, source})
Output: data/processed/    (train.jsonl, val.jsonl, optionally pushed to Hub)

Usage:
    python src/preprocess.py --data data/agri_qa.json --output data/processed/
    python src/preprocess.py --data data/agri_qa.json --output data/processed/ --push agroguardaiaOS/agroguardai-qa-dataset
"""

import argparse
import json
import random
from pathlib import Path

from datasets import Dataset, DatasetDict

# ── Chat template for instruction fine-tuning ──────────────────────────
SYSTEM_PROMPT = (
    "You are AgroguardAI, an agricultural assistant for smallholder farmers. "
    "You provide safe, evidence-based advice. When you lack information, "
    "you refuse to guess. You match the farmer's dialect and never recommend "
    "banned or dangerous products. Always cite your sources."
)

INSTRUCTION_TEMPLATE = (
    "A farmer asks the following question in {dialect} about {crop} in {region}. "
    "Respond with safe, practical agronomic advice in the same dialect.\n\n"
    "Farmer: {question}"
)


def format_conversation(entry: dict) -> dict:
    """Convert a raw dataset entry into a chat-format conversation."""
    instruction = INSTRUCTION_TEMPLATE.format(
        dialect=entry["dialect"],
        crop=entry["crop"],
        region=entry["region"],
        question=entry["question"],
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": instruction},
        {"role": "assistant", "content": entry["answer"]},
    ]
    return {"messages": messages}


def format_text(entry: dict, tokenizer_name: str = "") -> str:
    """
    Convert a chat entry to a single text string that can be tokenized.
    Uses the Mistral chat format by default; swap for other models.
    """
    msgs = entry["messages"]
    text = ""
    for m in msgs:
        role = m["role"]
        content = m["content"]
        if role == "system":
            text += f"<|system|>\n{content}</s>\n"
        elif role == "user":
            text += f"<|user|>\n{content}</s>\n"
        elif role == "assistant":
            text += f"<|assistant|>\n{content}</s>\n"
    return text


def load_and_format(data_path: Path) -> list[dict]:
    """Load raw JSON, apply chat formatting, return list of dicts."""
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    formatted = [format_conversation(entry) for entry in raw]
    for entry in formatted:
        entry["text"] = format_text(entry)
    return formatted


def split_dataset(entries: list[dict], val_ratio: float = 0.2, seed: int = 42) -> DatasetDict:
    """Randomly split into train / validation and return a DatasetDict."""
    random.seed(seed)
    indices = list(range(len(entries)))
    random.shuffle(indices)
    split = int(len(indices) * (1 - val_ratio))
    train_idx = sorted(indices[:split])
    val_idx = sorted(indices[split:])

    return DatasetDict({
        "train": Dataset.from_list([entries[i] for i in train_idx]),
        "validation": Dataset.from_list([entries[i] for i in val_idx]),
    })


def main():
    parser = argparse.ArgumentParser(description="Preprocess Agri-QA dataset")
    parser.add_argument("--data", required=True, help="Path to agri_qa.json")
    parser.add_argument("--output", required=True, help="Directory for processed files")
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--push", default="", help="Hugging Face Hub repo to push to")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    entries = load_and_format(Path(args.data))
    dataset = split_dataset(entries, val_ratio=args.val_ratio, seed=args.seed)

    # Save as JSONL
    for split_name, ds in dataset.items():
        path = out_dir / f"{split_name}.jsonl"
        ds.to_json(path, orient="records", lines=True, force_ascii=False)
        print(f"[✓] {split_name}: {len(ds)} samples → {path}")

    # Also save a combined dataset_info.json for reference
    info = {
        "num_train": len(dataset["train"]),
        "num_validation": len(dataset["validation"]),
        "format": "chat-messages + text field (Mistral tokenizer format)",
        "splits": ["train", "validation"],
    }
    (out_dir / "dataset_info.json").write_text(
        json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if args.push:
        dataset.push_to_hub(args.push)
        print(f"[✓] Pushed dataset to Hugging Face Hub: {args.push}")


if __name__ == "__main__":
    main()
