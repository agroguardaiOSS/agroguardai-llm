#!/usr/bin/env python3
"""Deduplicate and filter to Nigeria-only (Hausa, Igbo, Yoruba, Fulfulde)."""

import json
from collections import Counter

NIGERIAN_DIALECTS = {"Hausa", "Igbo", "Yoruba", "Fulfulde"}

with open("data/agri_qa.json", encoding="utf-8") as f:
    data = json.load(f)

before = len(data)

# ── 1. Keep only Nigerian entries ─────────────────────────────────
data = [e for e in data if e.get("dialect") in NIGERIAN_DIALECTS]
after_filter = len(data)
print(f"Filtered {before - after_filter} non‑Nigerian entries. {after_filter} remaining.")

# ── 2. Remove exact duplicates (same question text) ───────────────
seen = {}
clean = []
removed = 0
for e in data:
    q = e["question"].strip()
    if q in seen:
        removed += 1
    else:
        seen[q] = len(clean)
        clean.append(e)
print(f"Removed {removed} duplicates. Kept {len(clean)} entries.")

# ── 3. Re‑ID starting from agri‑001 ──────────────────────────────
for i, e in enumerate(clean):
    e["id"] = f"agri-{i + 1:04d}"   # agri‑0001, agri‑0002, ...

# ── 4. Save Nigeria‑only file ─────────────────────────────────────
with open("data/agri_qa_nigeria.json", "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=2, ensure_ascii=False)

# ── 5. Print summary ──────────────────────────────────────────────
dialects = Counter(e["dialect"] for e in clean)
crops = Counter(e["crop"] for e in clean)
print(f"\nFinal Nigeria‑only dataset: {len(clean)} entries")
print("Dialect distribution:")
for d, c in dialects.most_common():
    print(f"  {d}: {c}")
print("\nTop 10 crops:")
for crop, c in crops.most_common(10):
    print(f"  {crop}: {c}")
