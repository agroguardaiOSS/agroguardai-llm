#!/usr/bin/env python3
"""Load expansion entries from JSON and merge into agri_qa.json."""

import json, sys
from pathlib import Path
from collections import Counter

DATASET_PATH = Path("data/agri_qa.json")
EXPANSION_PATH = Path("data/expansion_entries.json")

with open(DATASET_PATH) as f:
    existing = json.load(f)

with open(EXPANSION_PATH) as f:
    new_entries = json.load(f)

existing_ids = {e["id"] for e in existing}
last_id = max(int(e["id"].replace("agri-", "")) for e in existing)
next_id = last_id + 1

# Assign fresh IDs
for entry in new_entries:
    eid = f"agri-{next_id}"
    next_id += 1
    while eid in existing_ids:
        next_id += 1
        eid = f"agri-{next_id}"
    existing_ids.add(eid)
    entry["id"] = eid

# Validate
valid_regions = {"Kenya", "Tanzania", "Uganda", "Ghana", "Rwanda"}
valid_dialects = {"Luo", "Swahili", "Kikuyu", "English", "Luganda", "Twi", "Kinyarwanda"}
for i, e in enumerate(new_entries):
    assert e["id"].startswith("agri-"), f"Bad ID: {e['id']}"
    region = e.get("region", "")
    if region not in valid_regions:
        for vr in valid_regions:
            if vr in region: e["region"] = vr; break
        else: print(f"WARNING: unexpected region '{region}' at idx {i}")
    assert 10 < len(e["question"]) < 600, f"Question bad length at idx {i}: {len(e['question'])}"
    assert 50 < len(e["answer"]) < 2500, f"Answer bad length at idx {i}: {len(e['answer'])}"
    assert len(e["source"]) > 10, f"Source too short at idx {i}"

# Count
regions = Counter(e["region"] for e in new_entries)
dialects = Counter(e["dialect"] for e in new_entries)
print(f"Generating {len(new_entries)} new entries")
print(f"Regions: {dict(regions)}")
print(f"Dialects: {dict(dialects)}")

# Merge
merged = existing + new_entries
with open(DATASET_PATH, "w") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Merged: {len(existing)} → {len(merged)} entries")

# Post-merge stats
rc = Counter(e["region"] for e in merged)
dc = Counter(e["dialect"] for e in merged)
print()
for r, n in rc.most_common():
    print(f"  {r:15s}: {n:4d}")
print(f"  {'TOTAL':15s}: {len(merged):4d}")
print(f"\n  Luo: {dc.get('Luo', 0)} entries (was 42)")
print(f"  Swahili: {dc.get('Swahili', 0)} entries (was 45)")
