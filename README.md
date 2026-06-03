# AgroguardAI-LLM

<p align="center">
  <strong>An open-source agricultural LLM that understands local dialects, crop science, and soil health — built because generic AI kills farmers.</strong>
</p>

---

## Why This Exists

Farmers in rural Nigeria, India, Kenya, and across the Global South rely on AI chatbots for
agronomic advice. The problem: **GPT-5, Claude, Grok, DeepSeek, and Gemini hallucinate
dangerously when asked about local crops, pests, and soil conditions.** They recommend
fertilizers unavailable in the region, misdiagnose cassava mosaic virus as potato blight,
prescribe banned pesticides, and fail to understand Hausa, Yoruba, Igbo, Swahili, or Pidgin.

**One wrong answer can destroy a season's harvest — or poison a community.**

AgroguardAI-LLM is a fine-tuned language model purpose-built for agriculture. It speaks local
dialects, knows the difference between maize streak virus and nitrogen deficiency, and returns
*refuse-to-answer* instead of guessing when it lacks evidence. No hallucinations. No generic
WebMD-for-plants nonsense. Just safe, grounded, farmer-first advice.

## What's Inside

```
agroguardai-llm/
├── README.md                  ← You are here
├── LICENSE                    ← Apache 2.0
├── requirements.txt           ← All Python dependencies
├── .gitignore                 ← Python + Hugging Face + model artefacts
├── config/
│   └── lora_config.yaml       ← LoRA hyperparameters (r, alpha, dropout, target modules)
├── data/
│   ├── README.md              ← Data collection logbook
│   ├── agri_qa.json           ← Seed dataset: 10 farmer Q&A pairs in dialect
│   └── processed/             ← Tokenized datasets land here (gitignored)
├── src/
│   ├── preprocess.py          ← Format → tokenize → push to Hub
│   ├── train.py               ← QLoRA fine-tuning (Mistral-7B / TinyLlama)
│   ├── inference.py           ← Load LoRA adapter → answer farmer questions
│   └── evaluate.py            ← Side-by-side eval against GPT-5, Claude, etc.
├── scripts/
│   ├── train.sh               ← One-command training entrypoint
│   ├── inference.sh           ← Interactive inference shell
│   └── evaluate.sh            ← Run the full cross-model benchmark
└── models/
    └── .gitkeep               ← Downloaded base models & saved adapters
```

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/agroguardaiaOS/agroguardai-llm.git
cd agroguardai-llm
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Inference (use a pre-trained LoRA adapter)

```bash
# Downloads Mistral-7B + your adapter, starts a REPL
bash scripts/inference.sh
```

Or programmatically:

```python
from src.inference import AgroguardInference

model = AgroguardInference(
    base_model="mistralai/Mistral-7B-Instruct-v0.3",
    adapter_path="agroguardaiaOS/agroguardai-llm-lora",  # your Hugging Face repo
)
answer = model.ask("My tomato leaf get black spot for underside. Wetin I fit do?")
print(answer)
```

### 3. Fine-Tune

```bash
# 1. Prepare data
python src/preprocess.py --data data/agri_qa.json --output data/processed/

# 2. Review LoRA config, then train
bash scripts/train.sh
```

Edit `config/lora_config.yaml` to switch between Mistral-7B and TinyLlama, adjust rank,
or toggle 4-bit quantization.

### 4. Evaluate

```bash
# Runs our model head-to-head against GPT-5, Claude, Grok, DeepSeek, Gemini
# on safety, dialect fidelity, and hallucination rate
bash scripts/evaluate.sh
```

## Results

*Placeholder — fill after your evaluation run.*

| Model | Safety (0–1) | Dialect Fidelity | Hallucination Rate | BLEU |
|-------|-------------|------------------|--------------------|------|
| **AgroguardAI-LLM** | — | — | — | — |
| GPT-5 | — | — | — | — |
| Claude 4 | — | — | — | — |
| Grok 3 | — | — | — | — |
| DeepSeek V3 | — | — | — | — |
| Gemini 2.5 Pro | — | — | — | — |

**Metrics:**
- **Safety** — Does the answer avoid dangerous or banned recommendations?
- **Dialect Fidelity** — Is the response in the same dialect the farmer used?
- **Hallucination Rate** — Fraction of claims not verifiable against agricultural reference.
- **BLEU** — Overlap with expert-written reference answer (useful but not sufficient alone).

## Dataset

The seed dataset (`data/agri_qa.json`) contains 10 realistic farmer questions spanning
multiple crops, regions, and dialects. Each entry includes:

- `id` — Unique identifier
- `region` — Country / growing zone
- `dialect` — Language or dialect the question was asked in
- `crop` — Target crop
- `question` — The farmer's exact words
- `answer` — A safe, evidence-backed response
- `source` — Reference (research paper, extension guide, agronomist review)

See `data/README.md` for the full collection log.

## Model

We fine-tune **Mistral-7B-Instruct-v0.3** (default) or **TinyLlama-1.1B** using QLoRA:

- 4-bit NF4 quantization of the base model
- Low-rank adapters on all linear projection layers
- Training on a single consumer GPU (RTX 3090/4090 or A10G)

The LoRA adapter is ~50 MB and can be shared on Hugging Face Hub alongside the base model ID.

## Roadmap

- [ ] Expand dataset to 1,000+ verified Q&A pairs across 10 languages
- [ ] Add vision encoder for crop disease photos
- [ ] Distill to a 1–3B model for on-device inference
- [ ] Integrate with WhatsApp and Telegram bots for direct farmer access
- [ ] Publish a peer-reviewed safety evaluation

## License

Apache 2.0 — see [LICENSE](./LICENSE).

## Citation

```bibtex
@software{agroguardai_llm,
  author = {AgroguardAI Contributors},
  title = {AgroguardAI-LLM: A Safety-First Agricultural Language Model},
  year = {2025},
  url = {https://github.com/agroguardaiaOS/agroguardai-llm}
}
```
