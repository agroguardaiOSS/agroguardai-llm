#!/usr/bin/env python3
"""
Automated Data Quality Checks for AgroGuardAI Agri-QA Dataset.

Runs multiple validation layers and generates a fresh coverage report:

  1. Schema validation (all 8 required fields + types)
  2. Duplicate detection (exact + near-duplicate via fuzzy matching)
  3. Safety checks (banned terms, dangerous patterns, source quality)
  4. Coverage gap analysis (crop x region x dialect matrix)
  5. Answer quality scoring (length, structure, numbered steps presence)
  6. ID consistency (sequential, no gaps, unique)

Output: JSON report file and human-readable summary.

Usage:
    python scripts/quality_check.py
    python scripts/quality_check.py --data data/agri_qa.json --output reports/quality_20260608.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = ["id", "region", "dialect", "crop", "question", "answer", "source"]
OPTIONAL_FIELDS = ["category"]

KNOWN_DIALECTS = {
    "Yoruba", "Pidgin English", "Hausa", "Swahili", "Hindi", "English",
    "Igbo", "Kikuyu", "Luo", "Punjabi", "Tamil", "Amharic",
    "Luganda", "Kinyarwanda",
    "Twi", "Fulfulde", "Kanuri", "Tiv", "Ibibio",
}

KNOWN_CROPS = {
    "cassava", "maize", "tomato", "rice", "cowpea", "mango", "yam",
    "sorghum", "millet", "groundnut", "banana", "sweet potato",
    "onion", "pepper", "okra", "amaranth", "cabbage", "watermelon",
    "coffee", "cocoa", "cotton", "cashew", "tea", "oil palm",
    "plantain", "beans", "sunflower",
    "dairy", "teff",
}

KNOWN_REGIONS = {
    "Nigeria", "Kenya", "India", "Ethiopia", "Tanzania",
    "Rwanda", "Ghana", "Malawi", "Uganda",
}

BANNED_TERMS = [
    "aldrin", "dieldrin", "endrin", "chlordane", "heptachlor",
    "lindane", "parathion", "methyl parathion", "monocrotophos",
    "methamidophos", "phosphamidon", "ddt",
]

DANGEROUS_PATTERNS = [
    (r"(apply|use|spray|mix).{0,30}(paracetamol|ibuprofen|aspirin|antibiotic)", "human medicine on crops"),
    (r"(without|no need).{0,30}(glove|mask|protection|ppe)", "discouraging PPE"),
    (r"double.{0,10}(dose|rate|amount|strength)", "recommending overdose"),
    (r"burn.{0,20}(tyre|tire|plastic|diesel|petrol|kerosene)", "burning hazardous materials"),
    (r"(apply|spray|use).{0,20}(diesel|petrol|kerosene).{0,20}(pesticide|insecticide|spray)", "fuel as pesticide"),
    (r"(?<!do not )(?<!don.t )(?<!never )(?<!avoid )(eat|chop|consume).{0,30}(rotten|spoiled|moldy|mouldy|diseased)", "eating unsafe produce"),
]

MIN_ANSWER_LENGTH = 100
MIN_QUESTION_LENGTH = 20
COVERAGE_WARN_THRESHOLD = 10  # flag crops/dialects/regions with <10 entries


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

class QualityReport:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict[str, Any] = {
            "total_entries": 0,
            "schema_errors": 0,
            "duplicates_found": 0,
            "near_duplicates_found": 0,
            "safety_violations": 0,
            "source_issues": 0,
            "answer_quality_issues": 0,
            "id_gaps": [],
        }
        self.coverage: dict[str, Any] = {}
        self.answer_quality_scores: list[dict] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)


def check_schema(data: list[dict], report: QualityReport):
    """Validate all required fields, types, and ID format."""
    for entry in data:
        eid = entry.get("id", "UNKNOWN")
        for field in REQUIRED_FIELDS:
            if field not in entry:
                report.error(f"[{eid}] Missing required field: '{field}'")
                report.stats["schema_errors"] += 1
            elif not isinstance(entry[field], str):
                report.error(f"[{eid}] Field '{field}' must be string, got {type(entry[field]).__name__}")
                report.stats["schema_errors"] += 1
            elif not entry[field].strip():
                report.error(f"[{eid}] Field '{field}' is empty")
                report.stats["schema_errors"] += 1

        # ID format
        if not re.match(r"^agri-\d{3,}$", eid):
            report.error(f"[{eid}] ID must match pattern 'agri-NNN'")
            report.stats["schema_errors"] += 1

        # Dialect check
        dialect = entry.get("dialect", "")
        if dialect and dialect not in KNOWN_DIALECTS:
            report.warn(f"[{eid}] Unknown dialect: '{dialect}'")

    # ID gaps (checks for missing sequential IDs)
    ids = sorted(int(e["id"].replace("agri-", "")) for e in data if e.get("id", "").startswith("agri-"))
    if ids:
        expected = list(range(ids[0], ids[-1] + 1))
        gaps = set(expected) - set(ids)
        if gaps:
            report.warn(f"ID gaps found: {sorted(gaps)[:20]}{'...' if len(gaps) > 20 else ''}")
            report.stats["id_gaps"] = sorted(gaps)


def check_duplicates(data: list[dict], report: QualityReport):
    """Detect exact and near-duplicate entries."""
    # Exact duplicates (same question text)
    questions = [e.get("question", "").strip() for e in data]
    q_counts = Counter(questions)
    exact_dups = {q: c for q, c in q_counts.items() if c > 1}
    if exact_dups:
        for q, c in exact_dups.items():
            report.error(f"Exact duplicate question ({c}×): '{q[:80]}...'")
        report.stats["duplicates_found"] = sum(c - 1 for c in exact_dups.values())

    # Near duplicates (fuzzy matching on question text)
    near_dup_count = 0
    SIMILARITY_THRESHOLD = 0.85
    for i in range(len(data)):
        q1 = data[i].get("question", "")
        for j in range(i + 1, len(data)):
            q2 = data[j].get("question", "")
            if abs(len(q1) - len(q2)) > len(q1) * 0.3:
                continue  # skip obviously different lengths
            sim = SequenceMatcher(None, q1.lower(), q2.lower()).ratio()
            if sim >= SIMILARITY_THRESHOLD:
                near_dup_count += 1
                if near_dup_count <= 10:  # cap warnings
                    report.warn(
                        f"Near-duplicate ({sim:.0%}): [{data[i].get('id')}] '{q1[:60]}...' "
                        f"≈ [{data[j].get('id')}] '{q2[:60]}...'"
                    )
    report.stats["near_duplicates_found"] = near_dup_count


def check_safety(data: list[dict], report: QualityReport):
    """Scan for banned terms and dangerous advice patterns."""
    for entry in data:
        eid = entry.get("id", "?")
        answer = entry.get("answer", "")
        answer_lower = answer.lower()

        for term in BANNED_TERMS:
            if term in answer_lower:
                report.error(f"[{eid}] BANNED PESTICIDE: '{term}' in answer")
                report.stats["safety_violations"] += 1

        for pattern, description in DANGEROUS_PATTERNS:
            if re.search(pattern, answer_lower):
                report.error(f"[{eid}] DANGEROUS ADVICE: {description}")
                report.stats["safety_violations"] += 1

        # Source quality
        source = entry.get("source", "")
        if len(source) < 10:
            report.warn(f"[{eid}] Source too short: '{source}'")
            report.stats["source_issues"] += 1
        weak_sources = ["internet", "common knowledge", "i think", "google", "chatgpt", "we think"]
        if any(w in source.lower() for w in weak_sources):
            report.error(f"[{eid}] Weak source: '{source}'")
            report.stats["source_issues"] += 1


def check_answer_quality(data: list[dict], report: QualityReport):
    """Score answer quality: length, structure, numbered steps."""
    for entry in data:
        eid = entry.get("id", "?")
        answer = entry.get("answer", "").strip()
        q = entry.get("question", "").strip()

        score = {
            "id": eid,
            "answer_length": len(answer),
            "question_length": len(q),
            "has_numbered_steps": bool(re.search(r"\(\d+\)", answer)),
            "has_source_citation": len(entry.get("source", "")) > 10,
            "flags": [],
        }

        if len(answer) < MIN_ANSWER_LENGTH:
            score["flags"].append("answer_too_short")
            report.warn(f"[{eid}] Answer too short ({len(answer)} chars)")
            report.stats["answer_quality_issues"] += 1

        if len(q) < MIN_QUESTION_LENGTH:
            score["flags"].append("question_too_short")

        if not score["has_numbered_steps"]:
            score["flags"].append("no_numbered_steps")

        report.answer_quality_scores.append(score)


def build_coverage_report(data: list[dict], report: QualityReport):
    """Generate a fresh coverage matrix: crop x region x dialect."""
    crop_counts = Counter(e.get("crop", "").lower() for e in data)
    dialect_counts = Counter(e.get("dialect", "") for e in data)
    region_counts = Counter(e.get("region", "") for e in data)
    category_counts = Counter(e.get("category", "unknown") for e in data)

    # Cross-matrix: (crop, region) → count
    combo_counts = Counter(
        (e.get("crop", "").lower(), e.get("region", "")) for e in data
    )

    # Thin coverage areas
    thin_crops = {c: n for c, n in crop_counts.items() if n < COVERAGE_WARN_THRESHOLD}
    thin_dialects = {d: n for d, n in dialect_counts.items() if n < COVERAGE_WARN_THRESHOLD}
    thin_regions = {r: n for r, n in region_counts.items() if n < COVERAGE_WARN_THRESHOLD}
    thin_combos = {(c, r): n for (c, r), n in combo_counts.items() if n < 3}

    # Missing from known sets
    missing_dialects = KNOWN_DIALECTS - set(dialect_counts.keys())
    missing_crops = KNOWN_CROPS - set(crop_counts.keys())
    missing_regions = KNOWN_REGIONS - set(region_counts.keys())

    report.coverage = {
        "total_entries": len(data),
        "crop_counts": dict(crop_counts.most_common()),
        "dialect_counts": dict(dialect_counts.most_common()),
        "region_counts": dict(region_counts.most_common()),
        "category_counts": dict(category_counts.most_common()),
        "unique_crops": len(crop_counts),
        "unique_dialects": len(dialect_counts),
        "unique_regions": len(region_counts),
        "thin_crops": thin_crops,
        "thin_dialects": thin_dialects,
        "thin_regions": thin_regions,
        "thin_crop_region_combos": len(thin_combos),
        "missing_in_known_dialects": sorted(missing_dialects),
        "missing_in_known_crops": sorted(missing_crops),
        "missing_in_known_regions": sorted(missing_regions),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AgroGuardAI data quality check")
    parser.add_argument("--data", default="data/agri_qa.json", help="Path to agri_qa.json")
    parser.add_argument("--output", default="", help="Output JSON path")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"ERROR: {data_path} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(data_path.read_text(encoding="utf-8"))
    print(f"[ ] Running quality checks on {len(data)} entries...")

    report = QualityReport()
    report.stats["total_entries"] = len(data)

    # Run all checks
    check_schema(data, report)
    check_duplicates(data, report)
    check_safety(data, report)
    check_answer_quality(data, report)
    build_coverage_report(data, report)

    # Compile output
    output: dict[str, Any] = {
        "date": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": report.stats,
        "errors": report.errors,
        "warnings": report.warnings,
        "coverage": report.coverage,
        "answer_quality_summary": {
            "avg_answer_length": round(
                sum(s["answer_length"] for s in report.answer_quality_scores) / max(len(report.answer_quality_scores), 1)
            ),
            "avg_question_length": round(
                sum(s["question_length"] for s in report.answer_quality_scores) / max(len(report.answer_quality_scores), 1)
            ),
            "with_numbered_steps": sum(1 for s in report.answer_quality_scores if s["has_numbered_steps"]),
            "with_source_citation": sum(1 for s in report.answer_quality_scores if s["has_source_citation"]),
            "flagged_answers": sum(1 for s in report.answer_quality_scores if s["flags"]),
        },
    }

    # Save
    out_path = args.output or f"reports/quality_{__import__('datetime').datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(output, open(out_path, "w"), indent=2, ensure_ascii=False)
    print(f"[✓] Quality report saved to: {out_path}")

    # Print summary
    s = report.stats
    c = report.coverage
    print(f"\n{'='*60}")
    print(f"  Data Quality Report — {len(data)} entries")
    print(f"{'='*60}")
    print(f"  Schema errors:       {s['schema_errors']}")
    print(f"  Exact duplicates:    {s['duplicates_found']}")
    print(f"  Near-duplicates:     {s['near_duplicates_found']}")
    print(f"  Safety violations:   {s['safety_violations']}")
    print(f"  Source issues:       {s['source_issues']}")
    print(f"  Answer quality flags:{s['answer_quality_issues']}")
    print(f"  ID gaps:             {len(s['id_gaps'])}")

    print(f"\n  Coverage:")
    print(f"    Crops:    {c['unique_crops']} ({len(c.get('thin_crops', {}))} thin)")
    print(f"    Dialects: {c['unique_dialects']} ({len(c.get('thin_dialects', {}))} thin)")
    print(f"    Regions:  {c['unique_regions']} ({len(c.get('thin_regions', {}))} thin)")
    print(f"    Thin crop×region combos: {c.get('thin_crop_region_combos', '?')}")

    if report.errors:
        print(f"\n  ⚠ ERRORS ({len(report.errors)}):")
        for e in report.errors[:10]:
            print(f"    {e}")
        if len(report.errors) > 10:
            print(f"    ... and {len(report.errors) - 10} more")

    if report.warnings:
        print(f"\n  ⚡ WARNINGS ({len(report.warnings)}):")
        for w in report.warnings[:10]:
            print(f"    {w}")
        if len(report.warnings) > 10:
            print(f"    ... and {len(report.warnings) - 10} more")

    thin_crops = c.get("thin_crops", {})
    if thin_crops:
        print(f"\n  📊 Thin crops (<{COVERAGE_WARN_THRESHOLD} entries):")
        for crop, n in sorted(thin_crops.items()):
            print(f"    {crop:20s}: {n:3d}")

    thin_dialects = c.get("thin_dialects", {})
    if thin_dialects:
        print(f"\n  📊 Thin dialects (<{COVERAGE_WARN_THRESHOLD} entries):")
        for d, n in sorted(thin_dialects.items()):
            print(f"    {d:25s}: {n:3d}")

    thin_regions = c.get("thin_regions", {})
    if thin_regions:
        print(f"\n  📊 Thin regions (<{COVERAGE_WARN_THRESHOLD} entries):")
        for r, n in sorted(thin_regions.items()):
            print(f"    {r:15s}: {n:3d}")

    exit_code = 1 if report.errors else 0
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
