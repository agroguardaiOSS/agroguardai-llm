#!/usr/bin/env bash
# ── AgroguardAI-LLM Evaluation Script ──────────────────────────────
# Benchmarks our model against GPT-5, Claude, Grok, DeepSeek, and Gemini.
#
# Requires API keys in environment:
#   OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, DEEPSEEK_API_KEY, XAI_API_KEY
#
# Usage:
#   bash scripts/evaluate.sh
#   bash scripts/evaluate.sh --models agroguardai,gpt5,claude

set -euo pipefail

echo "=============================================="
echo "  AgroguardAI-LLM — Cross-Model Evaluation"
echo "=============================================="

python src/evaluate.py \
    --data data/agri_qa.json \
    --output results/ \
    --verbose \
    "$@"

echo ""
echo "[✓] Full results saved to results/results.json and results/results.csv"
