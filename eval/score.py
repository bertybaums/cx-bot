#!/usr/bin/env python3
"""
CX-Bot Evaluation: Score generated completions (Tiers 1-2 + novelty).

Tier 1 — Structural:
  json_valid, fields_complete, conditions_count, passage_length,
  condition_overlap, bg_cases (AbdCx)

Tier 2 — Register & Style:
  hedging, british_spelling, no_forbidden

Novelty (optional):
  max TF-IDF cosine similarity to training passages

Usage:
    python eval/score.py \
        --input eval/results/completions.jsonl \
        --output eval/results/scored.jsonl

    # With novelty check against training data
    python eval/score.py \
        --input eval/results/completions.jsonl \
        --output eval/results/scored.jsonl \
        --training_dir data
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Tier 1: Structural ──

DEFCX_REQUIRED = ["definition", "conditions", "counterexample", "passage"]
ABDCX_REQUIRED = [
    "background_cases", "definition", "conditions",
    "counterexample", "abductive_insight", "passage",
]

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "and", "or", "but", "if",
    "that", "which", "who", "whom", "this", "these", "those", "it", "its",
    "of", "in", "on", "at", "to", "for", "with", "by", "from", "as",
    "into", "not", "no", "nor", "so", "yet", "he", "she", "they", "we",
    "his", "her", "their", "our", "my", "your", "one", "only",
}


def extract_keywords(text):
    """Extract content words (lowercase, >2 chars, no stop words)."""
    words = re.findall(r"[a-z]+", text.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


def condition_overlap(conditions, counterexample):
    """Fraction of conditions whose keywords appear in the counterexample."""
    if not conditions or not counterexample:
        return 0.0
    cx_kw = extract_keywords(counterexample)
    matched = sum(
        1 for c in conditions
        if extract_keywords(c) & cx_kw
    )
    return matched / len(conditions)


def try_parse_json(raw):
    """Try to parse JSON from raw model output, handling common issues."""
    text = raw.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last ``` lines
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting first JSON object
    brace_start = text.find("{")
    if brace_start >= 0:
        depth = 0
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[brace_start:i + 1])
                    except json.JSONDecodeError:
                        break

    return None


def score_structural(record):
    """Tier 1: structural validity checks."""
    scores = {}
    raw = record.get("raw_output", "")
    task = record.get("task_type", "DefCx")

    # 1. JSON validity
    parsed = try_parse_json(raw)
    scores["json_valid"] = parsed is not None
    if parsed is None:
        scores["tier1_pass"] = False
        return scores, None

    # 2. Required fields
    required = ABDCX_REQUIRED if task == "AbdCx" else DEFCX_REQUIRED
    missing = [f for f in required if f not in parsed]
    scores["fields_complete"] = len(missing) == 0
    scores["missing_fields"] = missing

    # 3. Conditions
    conds = parsed.get("conditions", [])
    if isinstance(conds, list):
        scores["conditions_count"] = len(conds)
    else:
        scores["conditions_count"] = 0
    scores["conditions_ok"] = scores["conditions_count"] >= 3

    # 4. Passage length
    passage = parsed.get("passage", "")
    words = passage.split() if isinstance(passage, str) else []
    scores["passage_words"] = len(words)
    min_words = 200 if task == "AbdCx" else 150
    scores["passage_length_ok"] = len(words) >= min_words

    # 5. Condition overlap
    cx_text = parsed.get("counterexample", "")
    if isinstance(conds, list) and isinstance(cx_text, str):
        scores["condition_overlap"] = round(condition_overlap(conds, cx_text), 3)
    else:
        scores["condition_overlap"] = 0.0
    scores["condition_overlap_ok"] = scores["condition_overlap"] >= 0.3

    # 6. AbdCx-specific: background cases
    if task == "AbdCx":
        bg = parsed.get("background_cases", [])
        scores["bg_cases_count"] = len(bg) if isinstance(bg, list) else 0
        scores["bg_cases_ok"] = scores["bg_cases_count"] >= 2

    # Composite
    checks = [
        scores["fields_complete"],
        scores["conditions_ok"],
        scores["passage_length_ok"],
        scores["condition_overlap_ok"],
    ]
    if task == "AbdCx":
        checks.append(scores.get("bg_cases_ok", False))
    scores["tier1_pass"] = all(checks)

    return scores, parsed


# ── Tier 2: Register & Style ──

HEDGING_PATTERNS = [
    r"one might (?:observe|note|suggest|argue|contend|say|think|suppose)",
    r"it (?:appears|seems|would seem) (?:that|as if|as though)",
    r"we should hesitate",
    r"upon (?:examination|reflection|consideration|closer inspection)",
    r"(?:perhaps|arguably|presumably|conceivably|admittedly)",
    r"it is (?:worth|important to) (?:not(?:ing|e)|observ(?:ing|e))",
    r"(?:consider|suppose|let us (?:imagine|consider|suppose))",
    r"one (?:may|might|could|would) (?:well |readily )?(?:ask|wonder|object|reply)",
]

BRITISH_WORDS = [
    "analyse", "analysed", "analysing", "behaviour", "defence", "favour",
    "favourable", "honour", "honourable", "colour", "labour", "neighbour",
    "recognise", "recognised", "recognising", "programme", "centre",
    "licence", "practise", "judgement", "whilst", "amongst", "towards",
    "fulfil", "enrol", "catalogue", "characterise", "characterised",
    "generalise", "generalised", "specialise", "specialised", "realise",
    "realised", "organise", "organised", "utilise", "utilised",
]

AMERICAN_WORDS = [
    "analyze", "analyzed", "analyzing", "behavior", "defense", "favor",
    "favorable", "honor", "honorable", "color", "labor", "neighbor",
    "recognize", "recognized", "recognizing", "program", "center",
    "license", "practice", "judgment", "while", "among", "toward",
    "fulfill", "enroll", "catalog", "characterize", "characterized",
    "generalize", "generalized", "specialize", "specialized", "realize",
    "realized", "organize", "organized", "utilize", "utilized",
]

FORBIDDEN_PATTERNS = [
    (r"(?m)^[\s]*[-*•]\s", "bullet_list"),
    (r"(?m)^#{1,6}\s", "markdown_header"),
    (r"\bcounterexample\b", "forbidden_word"),
    (r"\*\*[^*]+\*\*", "bold_markdown"),
    (r"\*[^*]+\*", "italic_markdown"),
]


def score_register(passage):
    """Tier 2: register and style compliance."""
    if not isinstance(passage, str) or not passage:
        return {"tier2_pass": False, "hedging_count": 0,
                "british_count": 0, "american_count": 0, "forbidden": []}

    scores = {}
    text_lower = passage.lower()

    # Hedging
    hedging_count = sum(
        1 for p in HEDGING_PATTERNS
        if re.search(p, passage, re.IGNORECASE)
    )
    scores["hedging_count"] = hedging_count
    scores["hedging_ok"] = hedging_count >= 2

    # British vs American spelling
    british = sum(1 for w in BRITISH_WORDS if w in text_lower)
    american = sum(1 for w in AMERICAN_WORDS if w in text_lower)
    scores["british_count"] = british
    scores["american_count"] = american
    # OK if any British found or no American found (short passages may have neither)
    scores["spelling_ok"] = british > 0 or american == 0

    # Forbidden patterns
    forbidden = []
    for pattern, label in FORBIDDEN_PATTERNS:
        if re.search(pattern, passage, re.IGNORECASE):
            forbidden.append(label)
    scores["forbidden"] = forbidden
    scores["register_clean"] = len(forbidden) == 0

    scores["tier2_pass"] = (
        scores["hedging_ok"]
        and scores["spelling_ok"]
        and scores["register_clean"]
    )
    return scores


# ── Novelty (TF-IDF) ──

def load_training_passages(data_dir):
    """Load all passages from training JSONL files."""
    passages = []
    for kind in ["defcx", "abdcx"]:
        d = Path(data_dir) / kind
        if not d.exists():
            continue
        for f in sorted(d.glob("*.jsonl")):
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    p = rec.get("passage", "")
                    if p:
                        passages.append(p)
    return passages


def compute_novelty(gen_passages, training_passages):
    """Compute max TF-IDF cosine similarity to training set for each generated passage."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        print("WARNING: scikit-learn not installed, skipping novelty check",
              file=sys.stderr)
        return [None] * len(gen_passages)

    all_passages = training_passages + gen_passages
    n_train = len(training_passages)

    vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")
    tfidf = vectorizer.fit_transform(all_passages)

    train_tfidf = tfidf[:n_train]
    gen_tfidf = tfidf[n_train:]

    similarities = []
    # Process in chunks to avoid memory issues
    chunk_size = 50
    for i in range(0, gen_tfidf.shape[0], chunk_size):
        chunk = gen_tfidf[i:i + chunk_size]
        sims = cosine_similarity(chunk, train_tfidf)
        for row in sims:
            similarities.append(round(float(row.max()), 4))

    return similarities


# ── Reporting ──

def print_report(scored_records):
    """Print a summary report of scored completions."""
    total = len(scored_records)
    if total == 0:
        print("No records to report.")
        return

    # Overall counts
    t1_pass = sum(1 for r in scored_records if r["scores"]["tier1_pass"])
    t2_pass = sum(1 for r in scored_records
                  if r["scores"].get("tier2_pass", False))
    both_pass = sum(1 for r in scored_records
                    if r["scores"]["tier1_pass"]
                    and r["scores"].get("tier2_pass", False))

    print(f"\n{'=' * 60}")
    print(f"CX-Bot Evaluation Report")
    print(f"{'=' * 60}")
    print(f"Total completions: {total}")
    print(f"Tier 1 pass: {t1_pass}/{total} ({100*t1_pass/total:.1f}%)")
    print(f"Tier 2 pass: {t2_pass}/{total} ({100*t2_pass/total:.1f}%)")
    print(f"Both pass:   {both_pass}/{total} ({100*both_pass/total:.1f}%)")

    # Tier 1 breakdown
    json_valid = sum(1 for r in scored_records
                     if r["scores"].get("json_valid", False))
    fields_ok = sum(1 for r in scored_records
                    if r["scores"].get("fields_complete", False))
    conds_ok = sum(1 for r in scored_records
                   if r["scores"].get("conditions_ok", False))
    passage_ok = sum(1 for r in scored_records
                     if r["scores"].get("passage_length_ok", False))
    overlap_ok = sum(1 for r in scored_records
                     if r["scores"].get("condition_overlap_ok", False))

    print(f"\nTier 1 Breakdown:")
    print(f"  JSON valid:       {json_valid}/{total} ({100*json_valid/total:.1f}%)")
    print(f"  Fields complete:  {fields_ok}/{total} ({100*fields_ok/total:.1f}%)")
    print(f"  Conditions ≥3:    {conds_ok}/{total} ({100*conds_ok/total:.1f}%)")
    print(f"  Passage length:   {passage_ok}/{total} ({100*passage_ok/total:.1f}%)")
    print(f"  Overlap ≥30%:     {overlap_ok}/{total} ({100*overlap_ok/total:.1f}%)")

    # Tier 2 breakdown
    hedge_ok = sum(1 for r in scored_records
                   if r["scores"].get("hedging_ok", False))
    spell_ok = sum(1 for r in scored_records
                   if r["scores"].get("spelling_ok", False))
    clean_ok = sum(1 for r in scored_records
                   if r["scores"].get("register_clean", False))

    print(f"\nTier 2 Breakdown:")
    print(f"  Hedging ≥2:       {hedge_ok}/{total} ({100*hedge_ok/total:.1f}%)")
    print(f"  Spelling OK:      {spell_ok}/{total} ({100*spell_ok/total:.1f}%)")
    print(f"  Register clean:   {clean_ok}/{total} ({100*clean_ok/total:.1f}%)")

    # Novelty stats
    novelty_scores = [r["scores"].get("max_tfidf_sim")
                      for r in scored_records
                      if r["scores"].get("max_tfidf_sim") is not None]
    if novelty_scores:
        avg_sim = sum(novelty_scores) / len(novelty_scores)
        max_sim = max(novelty_scores)
        memorized = sum(1 for s in novelty_scores if s >= 0.85)
        print(f"\nNovelty (TF-IDF similarity to training):")
        print(f"  Mean similarity:  {avg_sim:.3f}")
        print(f"  Max similarity:   {max_sim:.3f}")
        print(f"  Near-duplicates:  {memorized}/{len(novelty_scores)} "
              f"(≥0.85)")

    # Per-domain breakdown
    domain_stats = defaultdict(lambda: {"total": 0, "t1": 0, "t2": 0, "both": 0})
    for r in scored_records:
        d = r.get("domain", "unknown")
        domain_stats[d]["total"] += 1
        if r["scores"]["tier1_pass"]:
            domain_stats[d]["t1"] += 1
        if r["scores"].get("tier2_pass", False):
            domain_stats[d]["t2"] += 1
        if r["scores"]["tier1_pass"] and r["scores"].get("tier2_pass", False):
            domain_stats[d]["both"] += 1

    print(f"\nPer-Domain Pass Rates (Tier 1 / Tier 2 / Both):")
    for domain in sorted(domain_stats):
        s = domain_stats[domain]
        t = s["total"]
        print(f"  {domain:30s}  "
              f"{100*s['t1']/t:5.1f}%  {100*s['t2']/t:5.1f}%  "
              f"{100*s['both']/t:5.1f}%  (n={t})")

    # Per-task-type
    for task in ["DefCx", "AbdCx"]:
        subset = [r for r in scored_records if r.get("task_type") == task]
        if subset:
            tp = sum(1 for r in subset
                     if r["scores"]["tier1_pass"]
                     and r["scores"].get("tier2_pass", False))
            print(f"\n  {task}: {tp}/{len(subset)} "
                  f"({100*tp/len(subset):.1f}%) pass both tiers")

    print(f"\n{'=' * 60}\n")


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Score CX-Bot generated completions")
    parser.add_argument("--input", required=True,
                        help="Completions JSONL from generate.py")
    parser.add_argument("--output", default=None,
                        help="Scored JSONL output (default: <input>_scored.jsonl)")
    parser.add_argument("--training_dir", default=None,
                        help="Data directory for TF-IDF novelty check")
    parser.add_argument("--sim_threshold", type=float, default=0.85,
                        help="TF-IDF similarity threshold for memorization")
    args = parser.parse_args()

    if args.output is None:
        stem = Path(args.input).stem
        args.output = str(Path(args.input).parent / f"{stem}_scored.jsonl")

    # Load completions
    records = []
    with open(args.input) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loaded {len(records)} completions from {args.input}")

    # Score each record
    scored = []
    parsed_outputs = []
    for rec in records:
        t1_scores, parsed = score_structural(rec)

        # Tier 2: only if we got a parsed passage
        passage = parsed.get("passage", "") if parsed else ""
        t2_scores = score_register(passage)

        all_scores = {**t1_scores, **t2_scores}
        scored_rec = {**rec, "scores": all_scores}
        if parsed:
            scored_rec["parsed_output"] = parsed
        scored.append(scored_rec)
        parsed_outputs.append(passage if passage else "")

    # Novelty
    if args.training_dir:
        print("Computing TF-IDF novelty...")
        training_passages = load_training_passages(args.training_dir)
        print(f"  {len(training_passages)} training passages loaded")
        non_empty = [p for p in parsed_outputs if p]
        if non_empty:
            sims = compute_novelty(parsed_outputs, training_passages)
            for rec, sim in zip(scored, sims):
                rec["scores"]["max_tfidf_sim"] = sim
                if sim is not None:
                    rec["scores"]["novel"] = sim < args.sim_threshold

    # Write scored output
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        for rec in scored:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote scored results to {args.output}")

    # Report
    print_report(scored)


# Need os for makedirs
import os

if __name__ == "__main__":
    main()
