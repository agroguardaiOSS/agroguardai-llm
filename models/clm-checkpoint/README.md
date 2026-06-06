---
base_model: gpt2
library_name: peft
pipeline_tag: text-generation
tags:
- agriculture
- farming
- smallholder-farmers
- lora
- peft
- transformers
- nigerian-languages
- multilingual
- continued-pretraining
- crop-advisory
license: cc-by-4.0
datasets:
- AgroguardAI/agri-qa
language:
- yo
- ha
- ig
- pcm
- sw
- ki
- luo
- am
- hi
- pa
- ta
- en
---

# AgroguardAI CLM Agricultural GPT-2 (LoRA)

A proof-of-concept continued pre-training (CLM) of **GPT-2 (124M)** on the
[AgroguardAI Agri-QA dataset](https://huggingface.co/datasets/AgroguardAI/agri-qa)
using **LoRA adapters**. This model adapts base GPT-2 to the agricultural domain
across 12 dialects of Sub-Saharan Africa and South Asia.

> **This is a research prototype, NOT for production.** It was trained on CPU
> as a smoke test. The production target is Llama 3 8B with QLoRA on GPU.

## Model Details

- **Base model**: gpt2 (124M parameters, 12 layers, 768 hidden dim)
- **Adapter**: LoRA — rank=4, alpha=8, dropout=0.1
- **Trainable parameters**: 405,504 (0.33% of base model)
- **Training data**: 100 QA pairs from Agri-QA (80 train / 20 validation)
- **Training regime**: fp32, CPU, 50 steps, batch size 2, context window 1024 tokens
- **Training time**: ~30 seconds on CPU (proof-of-concept)

## Results

| Metric            | Value  |
|-------------------|--------|
| Final eval loss   | 4.64   |
| Perplexity        | 103.5  |

These numbers are from a minimal smoke test (50 steps on 80 training samples).
They are NOT indicative of what a properly-trained model can achieve. The
production pipeline targets < 10 perplexity on agricultural text.

## How to Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("gpt2")

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "AgroguardAI/clm-agricultural-gpt2-lora")
tokenizer = AutoTokenizer.from_pretrained("AgroguardAI/clm-agricultural-gpt2-lora")

# Generate agricultural text
prompt = "A farmer in Nigeria asks about cassava mosaic disease:"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100, do_sample=True, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Data

The model is trained on a 100-sample subset of the
[AgroguardAI Agri-QA dataset](https://huggingface.co/datasets/AgroguardAI/agri-qa)
— a curated, expert-annotated agricultural Q&A dataset covering 25 crops and
12 dialects across Nigeria, Kenya, India, Ethiopia, Tanzania, Ghana, Rwanda,
Malawi, and Uganda.

## Intended Uses

- **Domain adaptation research**: demonstrating how LoRA can cheaply adapt
  general-purpose LLMs to specialized agricultural domains
- **Baseline for future experiments**: establishing a bottom-line metric before
  scaling to larger models (Llama 3 8B, Mistral 7B)
- **Multilingual agricultural NLP**: evaluating how well base models handle
  low-resource languages (Yoruba, Hausa, Igbo, Kikuyu, Amharic, Luo, etc.)

## Out-of-Scope Uses

- **Production crop advisory** — DO NOT give real farming advice with this model.
  It is a prototype trained on 80 samples for 50 steps.
- **Safety-critical decisions** — the model may hallucinate or produce unsafe
  recommendations.

## Limitations

- **Tiny training run**: 50 steps, 80 samples — severe underfitting
- **CPU-only**: no mixed precision, no gradient accumulation, no LR scheduling
- **GPT-2 base**: a 2019 model with no instruction-following capability
- **High perplexity (103.5)**: the model is better than random but far from
  producing coherent agronomic advice
- **English-only tokenizer**: non-English text (Yoruba, Hausa, etc.) is
  poorly tokenized, increasing effective sequence length

## Environmental Impact

Negligible — the smoke test ran for ~30 seconds on a single CPU core.
Estimated < 0.001 kWh.

## Training Script

```bash
# Reproduce the training run:
python scripts/clm_pretrain.py \
  --data data/agri_qa.json \
  --output models/clm-checkpoint \
  --base-model gpt2 \
  --lora-rank 4 \
  --lora-alpha 8 \
  --batch-size 2 \
  --max-steps 50 \
  --val-samples 20 \
  --max-length 1024
```

Full source: https://github.com/agroguardaiOSS/agroguardai-llm

## Citation

```bibtex
@misc{agroguardai_clm_gpt2_lora_2025,
  title  = {AgroguardAI CLM Agricultural GPT-2 (LoRA)},
  author = {AgroguardAI},
  year   = {2025},
  url    = {https://huggingface.co/AgroguardAI/clm-agricultural-gpt2-lora}
}
```

## Model Card Authors

AgroguardAI Ecosystem — agroguardai1@gmail.com
