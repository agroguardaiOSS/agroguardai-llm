# AgroguardAI‑LLM

<p align="center">
  <strong>An open‑source agricultural LLM that bring safety in Agriculture  — built because generic AI gives farmers dangerous advice.</strong>
</p>

---

## Why This Exists

Smallholder farmers in Nigeria rely on AI chatbots for agronomic advice.  
The problem: **GPT‑5, Claude, Grok, DeepSeek, and Gemini hallucinate
dangerously when asked about local crops, pests, and soil conditions.**  
They recommend unavailable fertilisers, misdiagnose cassava mosaic, prescribe
banned pesticides, and fail completely on Hausa, Igbo, Yoruba, and Fulfulde.

**One wrong answer can destroy a season’s harvest — or poison a community.**

AgroguardAI‑LLM is a fine‑tuned language model purpose‑built for Nigerian agriculture.
It speaks the farmer’s language, knows the difference between maize streak virus
and nitrogen deficiency, and refuses to answer when it lacks evidence.
No hallucinations. No generic advice. Just safe, grounded, farmer‑first help.

## What’s Inside

```

agroguardai-llm/
├── README.md                      ← You are here
├── LICENSE                        ← Apache 2.0
├── requirements.txt
├── .gitignore
├── .github/workflows/
│   └── validate-qa.yml            ← CI: validates dataset schema & safety on every PR
├── configs/
│   └── llama3_qlora_v1.json       ← QLoRA config (presets for 3B / 8B)
├── data/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── qa_template.json
│   ├── agri_qa.json               ← full dataset (Nigeria‑only after cleaning)
│   ├── agri_qa_nigeria.json       ← filtered & deduplicated Nigeria‑only dataset
│   └── processed/                 ← tokenized train/test splits
├── notebooks/
│   └── colab_train.ipynb          ← one‑click training on free T4 GPU
├── scripts/
│   ├── finetune_llama3.py         ← QLoRA fine‑tuning (Llama‑3‑3B / 8B)
│   ├── evaluate_nigeria.py        ← safety, dialect, hallucination benchmark
│   ├── preprocess.py
│   ├── validate.py
│   └── generate_dataset.py
└── models/                        ← saved LoRA adapters & checkpoints

```

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/agroguardaiaOS/agroguardai-llm.git
cd agroguardai-llm
pip install -r requirements.txt
```

2. Inference

After training, you can load the LoRA adapter:

```bash
python scripts/finetune_llama3.py --help   # see all options
```

3. Train on a free T4 GPU (Colab)

https://colab.research.google.com/assets/colab-badge.svg

The notebook:

1. Installs dependencies
2. Clones the repo
3. Preprocesses the Nigeria‑only dataset
4. Runs QLoRA on Llama-3.2-3B-Instruct (T4‑friendly preset)
5. Saves the adapter to Google Drive
6. Optionally pushes it to Hugging Face Hub

4. Train Locally

```bash
# Preprocess the Nigeria‑only dataset
python scripts/preprocess.py --data data/agri_qa_nigeria.json --output data/processed/

# Start training with the 3B preset
python scripts/finetune_llama3.py --model-family llama3-3b --output ./models/llama3-agricultural-qlora
```

5. Evaluate

```bash
python scripts/evaluate_nigeria.py \
    --data data/processed/test_nigeria.json \
    --models agroguardai,gpt5,claude,gemini,grok,deepseek \
    --adapter ./models/llama3-agricultural-qlora \
    --output results/
```

Results

To be filled after the next evaluation run.

Model Safety (0–1) Dialect Fidelity Hallucination
AgroguardAI‑LLM — — —
GPT‑5 — — —
Claude — — —
Gemini — — —
Grok — — —
DeepSeek — — —

Metrics:

· Safety — Avoids banned substances, overdose, and missing PPE warnings.
· Dialect Fidelity — Response is in the same Nigerian language as the question.
· Hallucination — Claims are factually consistent with known agronomic references.

Dataset

The dataset (data/agri_qa_nigeria.json) contains farmer Q&A pairs in
Hausa, Igbo, Yoruba, and Fulfulde covering 25 crops across Nigeria.
All entries are reviewed by native speakers and agronomists for safety and
dialect accuracy. It is split into a training set and a held‑out test set.

Each entry includes:

· id — Unique identifier
· region — Nigeria
· dialect — Hausa, Igbo, Yoruba, or Fulfulde
· crop — Target crop
· question — The farmer’s exact words
· answer — A safe, evidence‑backed response in the same dialect
· source — Reference (extension guide, research paper, agronomist review)
· category — Pest Management, Disease Diagnosis, Soil Nutrition, Pesticide Safety, Cultural Practice, or Refusal
· safety_critical — Boolean flag for entries involving pesticide dosages

Model

We fine‑tune Llama‑3.2‑3B‑Instruct (and larger variants when compute permits)
using QLoRA:

· 4‑bit NF4 quantization
· Low‑rank adapters on all linear projection layers
· Training on a single T4 GPU (free Colab) or consumer hardware

The LoRA adapter is only a few megabytes and can be shared on Hugging Face Hub.

Roadmap

· Build Nigeria‑only dataset across 4 languages
· Prepare QLoRA fine‑tuning pipeline for Llama‑3
· Complete fine‑tuning and publish safety benchmark against GPT‑5 & Claude
· Expand Fulfulde coverage to 100+ entries
· Add vision encoder for crop disease photos
· Deploy to WhatsApp / Telegram for direct farmer access
· Publish a peer‑reviewed safety evaluation

License

Apache 2.0 — see LICENSE.

Citation

bibtex
@software{agroguardai_llm,
  author = {AgroguardAI Contributors},
  title = {AgroguardAI-LLM: A Safety-First Agricultural Language Model for Nigerian Languages},
  year = {2026},
  url = {https://github.com/agroguardaiaOS/agroguardai-llm}
}
