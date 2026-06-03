#!/usr/bin/env bash
# ── AgroguardAI-LLM Inference Script ───────────────────────────────
# Usage:
#   bash scripts/inference.sh                                   # interactive REPL
#   bash scripts/inference.sh --question "What is wrong with my maize?"

set -euo pipefail

BASE_MODEL="${AGROGUARD_BASE_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"
ADAPTER="${AGROGUARD_ADAPTER:-models/agroguardai-lora-adapter}"

python src/inference.py --base "$BASE_MODEL" --adapter "$ADAPTER" "$@"
