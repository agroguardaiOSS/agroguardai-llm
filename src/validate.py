"""
Schema and safety validator for AgroguardAI-LLM QA dataset.

Checks every entry in data/agri_qa.json for:
  1. Schema completeness (all 7 required fields, correct types)
  2. Unique IDs and sequential format
  3. Dialect validity (one of the known dialects)
  4. Crop validity (one of the known crops, lowercase)
  5. Safety rules (no banned pesticides, no dangerous advice patterns)
  6. Source quality (non-empty, reasonable format)
  7. Answer quality (minimum length, refusal detection)

Usage:
    python src/validate.py data/agri_qa.json
    python src/validate.py data/agri_qa.json --strict   # fail on warnings too

Exit code 0 = clean, 1 = errors found, 2 = strict mode warnings.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ["id", "region", "dialect", "crop", "question", "answer", "source"]

KNOWN_DIALECTS = {
    "Yoruba", "Pidgin English", "Hausa", "Swahili", "Hindi", "English",
    "Igbo", "Kikuyu", "Luo", "Punjabi", "Bengali", "Tamil", "Amharic",
    "Oromo", "Luganda", "Kinyarwanda", "Chichewa", "Bemba",
    "Spanish", "Portuguese", "Quechua", "French",
    "Twi",
    "Fulfulde", "Kanuri", "Tiv", "Ibibio",
}

KNOWN_CROPS = {
    "cassava", "maize", "tomato", "rice", "cowpea", "mango", "yam",
    "sorghum", "millet", "groundnut", "banana", "sweet potato", "irish potato",
    "onion", "pepper", "okra", "amaranth", "cabbage", "watermelon",
    "coffee", "cocoa", "cotton", "cashew", "tea", "oil palm",
    "plantain", "beans", "soybean", "sunflower", "coconut", "pigeon pea",
    "sugarcane", "wheat", "barley", "teff",
    "dairy",
}

BANNED_TERMS = [
    # WHO/FAO banned pesticides
    "aldrin", "dieldrin", "endrin", "chlordane", "heptachlor",
    "lindane", "parathion", "methyl parathion", "monocrotophos",
    "methamidophos", "phosphamidon", "ddt",
    # Dangerous application practices (patterns, not exact matches)
]

DANGEROUS_PATTERNS = [
    # Recommending human medicine on crops
    (r"(apply|use|spray|mix).{0,30}(paracetamol|ibuprofen|aspirin|antibiotic)", "human medicine on crops"),
    # No protective equipment warning with toxic chemicals
    (r"(without|no need).{0,30}(glove|mask|protection|ppe)", "discouraging PPE"),
    # Overdose recommendations
    (r"double.{0,10}(dose|rate|amount|strength)", "recommending overdose"),
    # Burning plastic/petroleum products
    (r"burn.{0,20}(tyre|tire|plastic|diesel|petrol|kerosene)", "burning hazardous materials"),
    # Recommending diesel/petrol as pesticide
    (r"(apply|spray|use).{0,20}(diesel|petrol|kerosene).{0,20}(pesticide|insecticide|spray)", "fuel as pesticide"),
    # Consuming unsafe parts
    (r"(?<!do not )(?<!don.t )(?<!never )(?<!avoid )(eat|chop|consume).{0,30}(rotten|spoiled|moldy|mouldy|diseased)", "eating unsafe produce (affirmative advice only)"),
]

MIN_ANSWER_LENGTH = 100  # characters — shorter answers are suspicious
MIN_QUESTION_LENGTH = 20  # characters

# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

class ValidationReport:
    """Collects errors and warnings, prints a summary, sets exit code."""

    def __init__(self, strict: bool = False):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.strict = strict
        self.file_path = ""

    def error(self, entry_id: str, msg: str):
        self.errors.append(f"[{entry_id}] ERROR: {msg}")

    def warn(self, entry_id: str, msg: str):
        self.warnings.append(f"[{entry_id}] WARNING: {msg}")

    def summary(self) -> int:
        print(f"\n{'='*60}")
        print(f"  Validation Report: {Path(self.file_path).name}")
        print(f"{'='*60}")

        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"    {e}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"    {w}")

        total_errors = len(self.errors)
        total_warnings = len(self.warnings)

        print(f"\n  {'✓' if total_errors == 0 else '✗'} {total_errors} error(s), {total_warnings} warning(s)")

        if total_errors > 0:
            print("  → Fix errors before submitting.\n")
            return 1
        if self.strict and total_warnings > 0:
            print("  → Strict mode: warnings treated as errors.\n")
            return 2
        print("  → Dataset is valid.\n")
        return 0


def validate_entry(entry: dict, idx: int, report: ValidationReport):
    """Run all checks on a single entry."""
    entry_id = entry.get("id", f"index_{idx}")

    # ── 1. Schema: all required fields present ─────────────────────────
    for field in REQUIRED_FIELDS:
        if field not in entry:
            report.error(entry_id, f"Missing required field: '{field}'")
            return  # can't continue without basic fields
        if not isinstance(entry[field], str):
            report.error(entry_id, f"Field '{field}' must be a string, got {type(entry[field]).__name__}")
            return
        if not entry[field].strip():
            report.error(entry_id, f"Field '{field}' is empty")

    # ── 2. ID format ───────────────────────────────────────────────────
    id_pattern = re.match(r"^agri-(\d{3,})$", entry["id"])
    if not id_pattern:
        report.error(entry_id, "ID must match pattern 'agri-NNN' (e.g. 'agri-001', 'agri-042')")

    # ── 3. Dialect check ───────────────────────────────────────────────
    if entry["dialect"] not in KNOWN_DIALECTS:
        report.warn(entry_id, f"Dialect '{entry['dialect']}' is not in the known list. Add it to KNOWN_DIALECTS in validate.py if it's correct.")

    # ── 4. Crop check ──────────────────────────────────────────────────
    crop_lower = entry["crop"].strip().lower()
    if entry["crop"] != crop_lower:
        report.error(entry_id, f"Crop '{entry['crop']}' must be lowercase (use '{crop_lower}')")
    if crop_lower not in KNOWN_CROPS:
        report.warn(entry_id, f"Crop '{crop_lower}' is not in the known list. Add it to KNOWN_CROPS in validate.py if it's correct.")

    # ── 5. Question length ─────────────────────────────────────────────
    if len(entry["question"].strip()) < MIN_QUESTION_LENGTH:
        report.error(entry_id, f"Question is too short ({len(entry['question'].strip())} chars). Minimum is {MIN_QUESTION_LENGTH}.")

    # ── 6. Answer length ───────────────────────────────────────────────
    answer_text = entry["answer"].strip()
    if len(answer_text) < MIN_ANSWER_LENGTH:
        report.error(entry_id, f"Answer is too short ({len(answer_text)} chars). Minimum is {MIN_ANSWER_LENGTH}. Farmer questions need thorough answers.")

    # ── 7. Safety: banned terms ────────────────────────────────────────
    answer_lower = answer_text.lower()
    for term in BANNED_TERMS:
        if term in answer_lower:
            report.error(entry_id, f"BANNED PESTICIDE: '{term}' appears in the answer. Remove immediately.")

    # ── 8. Safety: dangerous patterns ──────────────────────────────────
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, answer_lower):
            report.error(entry_id, f"DANGEROUS ADVICE: {description}")

    # ── 9. Source quality ──────────────────────────────────────────────
    source = entry["source"].strip()
    if len(source) < 10:
        report.warn(entry_id, f"Source is very short ('{source}'). Provide a proper reference (guide name, year, reviewer).")
    if any(weak in source.lower() for weak in ["internet", "common knowledge", "i think", "google", "chatgpt", "we think"]):
        report.error(entry_id, f"Weak source: '{source}'. Cite a specific extension guide, research paper, or named reviewer.")

    # ── 10. Refusal detection (not an error, just a classification note) ─
    refusal_indicators = [
        "cannot diagnose", "cannot accurately", "i lack", "do not have enough",
        "siwezi kukupa utambuzi", "basi siwezi", "extension office",
        "consult a local", "take a sample", "chukua sampuli",
    ]
    is_refusal = any(indicator in answer_lower for indicator in refusal_indicators)
    # Not an error — refusal entries are valuable. Just note it.
    if is_refusal:
        pass  # valid refusal entries are encouraged


def validate_dataset(data: list[dict], report: ValidationReport) -> int:
    """Run all checks across the full dataset."""

    if not isinstance(data, list):
        report.error("ROOT", "Dataset must be a JSON array")
        return 1

    if len(data) == 0:
        report.error("ROOT", "Dataset is empty — what are we validating?")
        return 1

    # ── Unique IDs ──────────────────────────────────────────────────────
    ids = []
    for entry in data:
        eid = entry.get("id", "")
        if eid:
            ids.append(eid)
    duplicates = {eid for eid in ids if ids.count(eid) > 1}
    for dup in sorted(duplicates):
        report.error(dup, f"Duplicate ID: '{dup}' appears {ids.count(dup)} times")

    # ── Validate each entry ─────────────────────────────────────────────
    for idx, entry in enumerate(data):
        validate_entry(entry, idx, report)

    # ── Coverage statistics ─────────────────────────────────────────────
    dialects_seen = {e.get("dialect", "") for e in data if e.get("dialect")}
    crops_seen = {e.get("crop", "").lower() for e in data if e.get("crop")}
    regions_seen = {e.get("region", "") for e in data if e.get("region")}

    print(f"\n  Dataset stats:")
    print(f"    Entries:  {len(data)}")
    print(f"    Dialects: {len(dialects_seen)} — {', '.join(sorted(dialects_seen))}")
    print(f"    Crops:    {len(crops_seen)} — {', '.join(sorted(crops_seen))}")
    print(f"    Regions:  {len(regions_seen)} — {', '.join(sorted(regions_seen))}")

    return report.summary()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Validate AgroguardAI-LLM QA dataset")
    parser.add_argument("file", help="Path to agri_qa.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)

    report = ValidationReport(strict=args.strict)
    report.file_path = str(path)
    exit_code = validate_dataset(data, report)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
