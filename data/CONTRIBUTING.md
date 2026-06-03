# Contributing QA Pairs to AgroguardAI-LLM

Thank you for helping grow a safety-first agricultural dataset that serves
smallholder farmers in their own languages. This guide tells you everything you
need to write a high-quality question-answer pair.

---

## Quick Checklist

Before you submit, make sure:

- [ ] The question is a **verbatim farmer question** — transcribed as spoken
- [ ] The answer **matches the farmer's dialect** (Yoruba question → Yoruba answer)
- [ ] The answer recommends **only safe, evidence-backed practices**
- [ ] Every claim is backed by a **cited source** (extension guide, research paper, agronomist)
- [ ] Banned or restricted pesticides/chemicals are **never** recommended
- [ ] When the answer is uncertain, it **refuses to guess** and suggests extension services
- [ ] The entry follows the exact JSON schema in `data/qa_template.json`

---

## Schema Reference

Every entry must have exactly these seven fields:

| Field    | Required | Description |
|----------|----------|-------------|
| `id`     | Yes      | Unique ID in the format `agri-NNN` (e.g. `agri-011`). Increment from the last entry. |
| `region` | Yes      | Country or growing zone (e.g. `"Nigeria"`, `"Kenya"`, `"India"`). |
| `dialect`| Yes      | The language/dialect of the question. Capitalise proper names: `"Yoruba"`, `"Pidgin English"`, `"Hausa"`, `"Swahili"`, `"Hindi"`, `"Igbo"`, `"English"`. |
| `crop`   | Yes      | Lowercase crop name: `"cassava"`, `"maize"`, `"tomato"`, `"rice"`, `"cowpea"`, `"mango"`, `"yam"`, `"sorghum"`, `"millet"`, `"groundnut"`, `"banana"`, `"coffee"`, `"cocoa"`, etc. |
| `question` | Yes    | The farmer's **exact words**, including greetings, code-switching, and non-standard grammar. Do NOT "clean up" the language. |
| `answer` | Yes      | A safe, evidence-backed response in the **same dialect as the question**. See answer rules below. |
| `source` | Yes      | Reference or reviewer name. Format: `"IITA Guide Name, Year; reviewed by Name, role"` or `"FAO Manual Name"`. |

---

## Answer Rules (Critical)

Every answer must satisfy these rules. The validation script enforces them
automatically, but you should internalise them as you write.

### 1. Dialect Match

The answer **must be in the same dialect** as the question. A Hausa question
gets a Hausa answer. A Pidgin question gets a Pidgin answer.

Do not answer a dialect question in English and then translate. The farmer asked
in their language — answer in their language.

### 2. Safety First

- **Never recommend banned or restricted pesticides.** The WHO/FAO ban list
  includes: DDT, aldrin, dieldrin, endrin, chlordane, heptachlor, lindane,
  parathion, methyl parathion, monocrotophos, methamidophos, phosphamidon.
  When in doubt, consult the [WHO
  list](https://www.who.int/news-room/fact-sheets/detail/pesticide-residues-in-food).
- **Never recommend unregistered or counterfeit products.**
- **Always include protective measures** when recommending any pesticide
  (gloves, mask, pre-harvest interval, keep away from children).
- **Prefer non-chemical controls first**: cultural practices, resistant
  varieties, biological controls, neem, ash, compost.

### 3. Evidence-Backed

Every claim must trace to a verifiable source:
- FAO, IITA, ICAR, KALRO, IRRI, CIMMYT, or other CGIAR centre guides
- Peer-reviewed agronomy or plant pathology papers
- National agricultural extension service bulletins
- Reviewed by a named agronomist or extension officer

If you cannot find a source for a claim, **do not make the claim**. Say "I
don't know" and direct the farmer to their local extension service.

### 4. Refuse to Guess

The model is trained to refuse unsafe answers. The dataset must teach that
boundary. Include entries where the correct answer is:

> "I cannot diagnose this from description alone. Please take a leaf sample to
> your nearest extension office for testing."

These refusal entries are as valuable as diagnostic ones — they teach the model
humility.

### 5. Practical & Actionable

Answers should:
- Start with the diagnosis in plain dialect
- Give numbered steps the farmer can do today
- Specify quantities (not "apply some" — give the rate per litre or per hectare)
- Mention timing (morning/evening, before/after rain, growth stage)
- Explain *why* each step works (builds farmer knowledge)

### 6. Source Citation

Every answer ends with a `source` field. Format examples:

Good:
```
"IITA Cassava Pest Management Guide, 2023; reviewed by Dr. A. Okeowo, agronomist"
"FAO Maize Disease Field Guide; cross-checked with KALRO extension bulletin"
"ICAR-IIHR Tomato Disease Guide; Indian Institute of Horticultural Research"
```

Bad:
```
"Internet"
"Common knowledge"
"We think so"
(blank)
```

---

## Dialect Guidelines

### Yoruba
- Yoruba uses tone marks. Include them if you can (è, é, ẹ, ọ, ṣ).
- Greetings are culturally important: "E ku agba mi" (respectful), "Bawo ni".
- Answers should use respectful register when addressing elder farmers.

### Pidgin English (West Africa)
- Not standard English. Preserve non-standard grammar: "e no grow well", "wetin I fit do?"
- Do not "correct" to standard English.
- Answers in Pidgin should use the same register: "Wetin you dey see na..."
- Common across Nigeria, Ghana, Sierra Leone, Liberia, Cameroon.

### Hausa
- Islamic greetings are common: "Assalamu alaikum" / "Wa alaikum assalam".
- Answers may mix Hausa with technical English terms for diseases/pests.
- Respectful address: use "Mallam" (Mr) or "Malama" (Mrs) where natural.

### Swahili (East Africa)
- Greet appropriately: "Habari" / "Nzuri" / "Shikamoo" (to elders).
- Swahili has noun classes — ensure agreement in answers.
- Common across Kenya, Tanzania, Uganda, Rwanda, DRC.

### Hindi (South Asia)
- Respectful address: "ji" suffix, "bhaiya" (brother), "didi" (sister).
- Mix of Hindi and English technical terms is natural.
- Use Devanagari-like transliteration: "kya", "hai", "karen".

### Igbo
- Greetings: "Ndewo" / "Kedu".
- Igbo is tonal — mark where possible (à, é, ò).
- Technical terms often appear in English within Igbo sentences.

### New Dialects
When adding a new dialect, follow these principles:
1. Preserve the farmer's exact words — including code-switching
2. Answer in the same dialect and register
3. Add the dialect name to the list above in a follow-up PR

---

## Crop Coverage Priorities

We are building a balanced dataset. Prioritise gaps:

| Priority | Crops |
|----------|-------|
| **Highest** (staple gaps) | yam, sorghum, millet, groundnut, banana, sweet potato |
| **High** (horticulture) | onion, pepper, okra, amaranth, cabbage, watermelon |
| **Medium** (cash crops) | coffee, cocoa, cotton, cashew, tea, oil palm |
| **Lower** (already covered) | maize, cassava, tomato, rice, cowpea, mango |

---

## Regional Coverage Priorities

| Priority | Regions |
|----------|---------|
| **Highest** | Nigeria (Hausa belt, Igbo southeast), Ethiopia, Tanzania, Uganda |
| **High** | Ghana, Mali, Burkina Faso, Rwanda, Malawi, Zambia |
| **Medium** | India (Punjab, Tamil Nadu, West Bengal), Bangladesh, Nepal |
| **Future** | Latin America (Spanish, Portuguese, Quechua), Southeast Asia |

---

## How to Submit

1. **Fork** the repository at `github.com/agroguardaiaOS/agroguardai-llm`
2. **Copy** `data/qa_template.json` and fill in your QA pair(s)
3. **Append** your entries to `data/agri_qa.json` (keep all existing entries)
4. **Run** the validator: `python src/validate.py data/agri_qa.json`
5. **Fix** any validation errors and re-run until clean
6. **Open a Pull Request** with a title like `qa: add 3 Yoruba cassava pairs` or `qa: add 5 Swahili maize entries`

A maintainer will review your submission for accuracy and safety before merging.

---

## Review Process

Every submission is checked for:

1. **Schema compliance** (automated via `src/validate.py` and GitHub Actions)
2. **Safety** — no banned products, no dangerous advice (manual review)
3. **Accuracy** — diagnosis matches symptoms, treatment is evidence-backed
4. **Dialect quality** — answer is idiomatic and natural in the target dialect
5. **Source quality** — every answer cites a credible reference

---

## Example: Good Entry

```json
{
  "id": "agri-011",
  "region": "Nigeria",
  "dialect": "Pidgin English",
  "crop": "cassava",
  "question": "My cassava root dey soft and e get bad smell when I harvest. The leaf still green o, but inside the root don spoil. Wetin cause am?",
  "answer": "Wetin you dey describe na cassava root rot, and e get two kind wey common: (1) Soft rot wey bacteria dey cause — this one dey happen when water stand for the field too long, or when you harvest and the root stay for wet ground. The smell na sign say bacteria don enter. (2) Root rot wey fungi dey cause — this one dey show brown dry patches inside the root before the soft stage. Wetin to do: First thing, harvest every mature cassava NOW — the longer they stay, the more go spoil. Dig drainage channels around your field to carry water comot. For the cassava wey remain, apply Trichoderma powder (biological fungicide) to the soil around the stem base — this fungus dey fight the rot fungus for ground. Next season: plant on ridges (not flat ground), use TME 419 variety (e resistant to root rot), and rotate to a legume like cowpea for at least one season before you plant cassava for that same land again. No chop or sell the rotten roots — bury them far from the field.",
  "source": "IITA Cassava Root Rot Management Guide; NRCRI Umudike extension bulletin; reviewed by cassava pathologist"
}
```

---

## Example: Good Refusal Entry

```json
{
  "id": "agri-012",
  "region": "Kenya",
  "dialect": "Swahili",
  "crop": "maize",
  "question": "Mahindi yangu hayakua vizuri na majani yana rangi ya zambarau. Nilitumia mbolea ya DAP lakini haikusaidia. Kuna mtu alisema ni ugonjwa wa virusi, mwingine akasema ni upungufu wa virutubisho. Nifanye nini?",
  "answer": "Shikamoo. Rangi ya zambarau kwenye majani ya mahindi inaweza kuwa na sababu nyingi — inaweza kuwa upungufu wa fosforasi, au ugonjwa wa virusi, au hata uharibifu wa mizizi kutoka kwa wadudu wa ardhini. Mimea inayoonyesha dalili za aina moja inaweza kuwa na matatizo tofauti kabisa. Kwa sababu hii, siwezi kukupa utambuzi sahihi kutoka kwa maelezo pekee. Hiki ndicho unachopaswa kufanya: Chukua mimea michache yenye dalili (pamoja na mizizi) na upeleke katika ofisi ya karibu ya kilimo ya kaunti (county extension office) au KALRO. Waambie historia yote — tarehe ya kupanda, mbolea uliyotumia, na mwelekeo wa dalili. Watachunguza na kukupa ushauri sahihi. Usitumie dawa yoyote kabla ya kupata utambuzi sahihi — inaweza kuwa upotevu wa pesa na inaweza kuharibu mazingira.",
  "source": "KALRO Maize Diagnostics Protocol; FAO Guide to Nutrient Deficiency Identification"
}
```

---

*Last updated: 2025-06-03*
