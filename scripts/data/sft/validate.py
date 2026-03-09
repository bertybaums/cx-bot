#!/usr/bin/env python3
"""
Structural validation of generated SFT examples.

Generalised from the gettier project — no epistemology exclusion filter.

Checks:
  - Required fields present
  - conditions is a list of >= 2 strings
  - passage text >= 100 characters
  - Counterexample references stated conditions (keyword overlap)
  - AbdCx: background_cases is list of >= 2, abductive_insight present
  - Deduplication via TF-IDF cosine similarity

Usage:
    python scripts/data/sft/validate.py \
        --input data/sft/defcx.jsonl \
        --output data/sft/defcx_validated.jsonl \
        --report data/sft/defcx_validation_report.txt
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.data.sft.domains import all_domain_names


# ── Required fields by dataset type ──

DEFCX_REQUIRED = {
    "id", "domain", "subdomain", "definition", "conditions",
    "counterexample", "passage",
}

ABDCX_REQUIRED = DEFCX_REQUIRED | {
    "background_cases", "abductive_insight",
}


def detect_dataset_type(record):
    """Infer whether a record is DefCx or AbdCx."""
    if "background_cases" in record or "abductive_insight" in record:
        return "abdcx"
    return "defcx"


def validate_record(record, idx):
    """Validate a single record. Returns (is_valid, list_of_issues)."""
    issues = []
    dataset_type = detect_dataset_type(record)
    required = ABDCX_REQUIRED if dataset_type == "abdcx" else DEFCX_REQUIRED

    # Check required fields
    missing = required - set(record.keys())
    if missing:
        issues.append(f"missing fields: {sorted(missing)}")

    # Check domain
    rec_id = record.get("id", f"record_{idx}")
    domain = record.get("domain", "")
    valid_domains = all_domain_names()
    if domain and domain not in valid_domains:
        issues.append(f"unknown domain: '{domain}'")

    # Check conditions
    conditions = record.get("conditions", [])
    if not isinstance(conditions, list):
        issues.append("conditions is not a list")
    elif len(conditions) < 2:
        issues.append(f"conditions has {len(conditions)} items (need >= 2)")
    elif not all(isinstance(c, str) and len(c) > 0 for c in conditions):
        issues.append("conditions contains non-string or empty entries")

    # Check passage length
    passage = record.get("passage", "")
    if not isinstance(passage, str):
        issues.append("passage is not a string")
    elif len(passage) < 100:
        issues.append(f"passage too short ({len(passage)} chars, need >= 100)")

    # Check counterexample references conditions
    counterexample = record.get("counterexample", "")
    if isinstance(counterexample, str) and isinstance(conditions, list):
        overlap = _condition_overlap(counterexample, conditions)
        if overlap < 0.3:
            issues.append(
                f"counterexample has low condition overlap "
                f"({overlap:.0%}; at least 30% expected)"
            )

    # AbdCx-specific checks
    if dataset_type == "abdcx":
        bg = record.get("background_cases", [])
        if not isinstance(bg, list):
            issues.append("background_cases is not a list")
        elif len(bg) < 2:
            issues.append(
                f"background_cases has {len(bg)} items (need >= 2)"
            )

        insight = record.get("abductive_insight", "")
        if not isinstance(insight, str) or len(insight) < 10:
            issues.append("abductive_insight missing or too short")

    return len(issues) == 0, issues


def _condition_overlap(counterexample, conditions):
    """Fraction of conditions whose key terms appear in the counterexample."""
    if not conditions:
        return 1.0

    cx_words = set(re.findall(r"\b\w+\b", counterexample.lower()))
    matched = 0
    for cond in conditions:
        cond_words = set(re.findall(r"\b\w+\b", cond.lower()))
        # Remove stop words
        cond_words -= {
            "a", "an", "the", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "and",
            "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "by", "from", "it", "its", "that", "this", "not", "no",
        }
        if not cond_words:
            matched += 1
            continue
        if cx_words & cond_words:
            matched += 1

    return matched / len(conditions)


# ── TF-IDF deduplication ──

def _tokenize(text):
    """Simple whitespace + lowering tokeniser."""
    return re.findall(r"\b\w+\b", text.lower())


def _build_tfidf(passages):
    """Build TF-IDF vectors for a list of passages.

    Returns list of (Counter, norm) tuples.
    """
    n_docs = len(passages)
    if n_docs == 0:
        return []

    # Document frequencies
    df = Counter()
    doc_tfs = []
    for p in passages:
        tokens = _tokenize(p)
        tf = Counter(tokens)
        doc_tfs.append(tf)
        df.update(set(tokens))

    # Compute TF-IDF vectors (as sparse Counters) and norms
    vectors = []
    for tf in doc_tfs:
        tfidf = {}
        norm_sq = 0.0
        for term, count in tf.items():
            idf = math.log(n_docs / (1 + df[term]))
            val = count * idf
            tfidf[term] = val
            norm_sq += val * val
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        vectors.append((tfidf, norm))

    return vectors


def _cosine_sim(vec_a, norm_a, vec_b, norm_b):
    """Cosine similarity between two sparse vectors."""
    dot = 0.0
    # Iterate over smaller vector
    if len(vec_a) > len(vec_b):
        vec_a, norm_a, vec_b, norm_b = vec_b, norm_b, vec_a, norm_a
    for term, val_a in vec_a.items():
        if term in vec_b:
            dot += val_a * vec_b[term]
    return dot / (norm_a * norm_b)


def find_duplicates(records, threshold=0.85):
    """Find near-duplicate pairs by TF-IDF cosine similarity on passages.

    Returns list of (idx_a, idx_b, similarity) tuples.
    """
    passages = [r.get("passage", "") for r in records]
    vectors = _build_tfidf(passages)

    duplicates = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            sim = _cosine_sim(
                vectors[i][0], vectors[i][1],
                vectors[j][0], vectors[j][1],
            )
            if sim >= threshold:
                duplicates.append((i, j, sim))

    return duplicates


# ── Main validation pipeline ──

def validate_file(input_path, output_path=None, report_path=None,
                  dedup_threshold=0.85):
    """Validate all records in a JSONL file.

    Returns (valid_records, report_lines).
    """
    input_path = Path(input_path)
    records = []
    parse_errors = 0

    with open(input_path) as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                parse_errors += 1

    report = []
    report.append(f"Validation report for {input_path}")
    report.append(f"Total records: {len(records)}")
    if parse_errors:
        report.append(f"Parse errors (skipped): {parse_errors}")
    report.append("")

    # Per-record validation
    valid_records = []
    invalid_records = []

    for idx, rec in enumerate(records):
        is_valid, issues = validate_record(rec, idx)
        rec_id = rec.get("id", f"record_{idx}")
        if is_valid:
            valid_records.append(rec)
        else:
            invalid_records.append((rec_id, issues))
            report.append(f"INVALID {rec_id}:")
            for issue in issues:
                report.append(f"  - {issue}")

    report.append("")
    report.append(f"Valid: {len(valid_records)}")
    report.append(f"Invalid: {len(invalid_records)}")

    # Deduplication check on valid records
    if len(valid_records) > 1:
        dupes = find_duplicates(valid_records, threshold=dedup_threshold)
        if dupes:
            report.append(f"\nNear-duplicates found ({len(dupes)} pairs, "
                          f"threshold={dedup_threshold}):")
            # Mark later duplicates for removal
            dup_indices = set()
            for i, j, sim in dupes:
                id_i = valid_records[i].get("id", f"record_{i}")
                id_j = valid_records[j].get("id", f"record_{j}")
                report.append(f"  {id_i} ~ {id_j} (sim={sim:.3f})")
                dup_indices.add(j)  # Remove the later one

            deduped = [
                r for idx, r in enumerate(valid_records)
                if idx not in dup_indices
            ]
            report.append(f"After deduplication: {len(deduped)} "
                          f"(removed {len(dup_indices)})")
            valid_records = deduped

    # Domain distribution
    domain_counts = Counter(r.get("domain", "unknown") for r in valid_records)
    report.append("\nDomain distribution:")
    for domain, count in sorted(domain_counts.items()):
        report.append(f"  {domain}: {count}")

    report_text = "\n".join(report)
    print(report_text)

    # Write outputs
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            for rec in valid_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"\nWrote {len(valid_records)} validated records to {output_path}")

    if report_path:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            f.write(report_text + "\n")
        print(f"Wrote report to {report_path}")

    return valid_records, report


def main():
    parser = argparse.ArgumentParser(
        description="Validate SFT dataset examples")
    parser.add_argument(
        "--input", required=True,
        help="Input JSONL file to validate")
    parser.add_argument(
        "--output", default=None,
        help="Output JSONL file for validated examples")
    parser.add_argument(
        "--report", default=None,
        help="Output path for validation report")
    parser.add_argument(
        "--dedup-threshold", type=float, default=0.85,
        help="Cosine similarity threshold for deduplication (default: 0.85)")

    args = parser.parse_args()
    validate_file(args.input, args.output, args.report, args.dedup_threshold)


if __name__ == "__main__":
    main()
