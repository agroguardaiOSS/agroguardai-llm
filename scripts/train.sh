#!/usr/bin/env bash
# ── AgroguardAI-LLM Training Script ────────────────────────────────
# Usage: bash scripts/train.sh [--config config/lora_config.yaml]
#
# Pre-requisites:
#   1. pip install -r requirements.txt
#   2. python src/preprocess.py --data data/agri_qa.json --output data/processed/

set -euo pipefail

CONFIG="${1:-config/lora_config.yaml}"

echo "=============================================="
echo "  AgroguardAI-LLM — Fine-Tuning"
echo "  Config: $CONFIG"
echo "=============================================="

# Ensure processed data exists
if [ ! -f data/processed/train.jsonl ]; then
    echo "[!] Processed data not found. Running preprocessing..."
    python src/preprocess.py --data data/agri_qa.json --output data/processed/
fi

python src/train.py --config "$CONFIG"
