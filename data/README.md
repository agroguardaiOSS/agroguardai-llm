# Data Collection Log — AgroguardAI-LLM

## Overview

This dataset is a seed collection of farmer questions paired with safe, evidence-backed
agronomic answers. It serves as both a starting point for fine-tuning and a template for
contributors who want to submit additional Q&A pairs.

## Collection Methodology

1. **Sources** — Questions were gathered from agricultural extension officers in
   Oyo State (Nigeria), Nakuru County (Kenya), and Punjab (India). Each officer
   transcribed verbatim questions they received from smallholder farmers during
   the 2024 growing season.

2. **Answer drafting** — Answers were written by an agronomist with 8+ years of
   field experience, then cross-checked against FAO and IITA extension guides.

3. **Dialect preservation** — Questions are transcribed exactly as spoken,
   including code-switching. Answers match the dialect of the question.

4. **Safety review** — Every answer was checked against the WHO/FAO pesticide
   ban list, local fertilizer regulations, and standard organic practice.

## Current Status

| Metric | Value |
|--------|-------|
| Total Q&A pairs | 10 |
| Languages / dialects | Hausa, Yoruba, Pidgin English, Swahili, Hindi, English |
| Crops covered | Maize, cassava, tomato, rice, cowpea, mango |
| Regions | Nigeria, Kenya, India, Ghana |
| Review status | Agronomist-reviewed |

## Format

Each entry in `agri_qa.json` follows this schema:

```json
{
  "id": "agri-001",
  "region": "Nigeria",
  "dialect": "Yoruba",
  "crop": "cassava",
  "question": "Farmer's exact words...",
  "answer": "Safe, evidence-backed response...",
  "source": "Reference or reviewer name"
}
```

## Planned Expansions

- [ ] 100+ Q&A pairs across West Africa (priority)
- [ ] East Africa dataset (Swahili, Kikuyu, Luo)
- [ ] South Asia dataset (Hindi, Punjabi, Bengali, Tamil)
- [ ] Latin America dataset (Spanish, Portuguese, Quechua)
- [ ] Expert adversarial questions (edge cases designed to trigger hallucinations)
- [ ] Crop-specific subsets: rice blast, cassava diseases, tomato pests

## Contributors

- AgroguardAI team (agronomist review)
- Extension officers from Oyo State ADP, Nigeria
- Extension officers from Nakuru County, Kenya
- Punjab Agricultural University extension network

---

*Last updated: 2025-06-03*
