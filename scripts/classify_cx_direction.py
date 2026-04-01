#!/usr/bin/env python3
"""
Classify each counterexample as demonstrating the definition is:
  - TOO WEAK (insufficient): all conditions hold, concept fails → definition lets in cases it shouldn't
  - TOO STRONG (over-restrictive): concept applies, but conditions exclude it → definition rules out cases it shouldn't
  - BOTH: counterexample reveals weakness in both directions
  - AMBIGUOUS: can't confidently classify

Uses heuristic keyword analysis on `missing_condition`, `passage`, and `counterexample` fields.
"""

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# --- Heuristic keyword patterns ---

# Signals that the definition is TOO WEAK (insufficient / lets in bad cases)
# Pattern: all conditions hold, but the concept doesn't apply → definition is too permissive
TOO_WEAK_PATTERNS = [
    # Explicit insufficiency language
    r"\binsufficien",
    r"\bnot sufficient\b",
    r"\btoo (?:broad|permissive|liberal|inclusive|lax|lenient|loose)\b",
    r"\bthe analysis (?:is |proves )?too (?:broad|permissive|liberal|inclusive)",
    # Conditions met + concept fails
    r"\ball (?:three|four|five|the stated|the enumerated)?\s*conditions (?:are |may be )?(?:met|satisfied|hold|fulfilled)",
    r"\bsatisf(?:y|ies) (?:all|each|every)\b.*\bcondition",
    r"\bconditions.*\b(?:hold|met|satisfied)\b.*\byet\b",
    r"\bconditions? (?:are |is )?met.*\byet\b",
    r"\bconditions? (?:are |is )?satisfied.*\byet\b",
    r"\bthe (?:three|four|five) conditions are (?:met|satisfied)",
    # Definition lets in bad cases
    r"\bpermit(?:s|ting)?\s+cases",
    r"\blets? in\b",
    r"\badmits? cases\b",
    # Something is missing / omitted
    r"\bomits? (?:any |the )?requirement",
    r"\blacks?\b.*\bcondition",
    r"\bmissing.*\brequirement",
    r"\bneeds? (?:a |an )?(?:additional|further|extra)\b",
    r"\brequires? (?:a |an )?(?:additional|further|extra)\b",
    r"\bno (?:requirement|condition|clause)\b.*\b(?:connect|link|relation)",
    r"\bneglects? to demand",
    # Fails to require/exclude/account (definition should have blocked this case)
    r"\bfails to (?:require|demand|capture|record|ensure|exclude|rule out|stipulat|account|address)",
    r"\bdoes not (?:require|demand|insist|stipulate)\b",
    # "What is missing / what the definition dropped"
    r"\bwhat (?:is |the definition |the analysis )?(?:missing|dropped|lost|omitted|left out)",
    r"\bthe (?:definition|analysis|account) (?:has )?dropped\b",
]

# Signals that the definition is TOO STRONG (over-restrictive / rules out good cases)
# Pattern: concept genuinely applies, but one or more conditions aren't met → definition is too restrictive
TOO_STRONG_PATTERNS = [
    # Explicit restrictiveness language
    r"\btoo (?:restrictive|stringent|narrow|demanding|strong|strict|rigid|exclusive|exacting|austere|severe)\b",
    r"\bover-?(?:restrictive|demanding|strict|narrow)\b",
    r"\bunduly\b.*\b(?:restrict|narrow|exclud|limit|constrain)",
    # Excludes / rules out genuine cases
    r"\bexcludes? (?:cases|instances|examples|scenarios|things|items|entities|what|a class|works|those)\b",
    r"\brules? out\b.*\b(?:genuine|legitimate|paradigm|clear|obvious|authentic|bona fide)\b",
    r"\b(?:genuine|legitimate|paradigm|clear|obvious|authentic|bona fide)\b.*\brules? out\b",
    r"\bfails? to (?:accommodate|include|admit|count|classify)\b",
    # "The definition requires X, but [X isn't actually necessary]"
    r"(?:the )?definition (?:requires|demands|insists)\b.*\bbut\b",
    r"(?:the )?definition (?:has )?(?:wrongly|incorrectly|mistakenly|erroneously)\b",
    r"(?:the )?definition (?:wrongly |incorrectly |mistakenly )?(?:equates?|ties?|models?|confuses?|assumes?|insists?)\b",
    r"(?:the )?definition (?:has )?(?:confused|assumed|supposed|taken for granted)\b",
    # Condition not met, yet concept applies
    r"\b(?:would |should |must |ought to )(?:still |yet |nevertheless |nonetheless )?(?:count|qualify|be (?:regarded|considered|classified))\b",
    r"\bthe condition.*\bis not (?:met|satisfied)\b.*\byet\b",
    r"\bnot (?:all |every )?conditions? (?:are |is )?(?:met|satisfied|fulfilled)\b",
    # "X may [also/instead] consist in / emerge from / operate through" (condition isn't necessary)
    r"\bmay (?:also |instead )?(?:consist in|emerge from|operate through|manifest as|be (?:constituted|exercised|expressed))\b",
    r"\bmay (?:be )?(?:exercised|directed|sustained|developed)\b.*\bwithout\b",
    # "Cannot accommodate" / "does not accommodate"
    r"\bcannot accommodate\b",
    r"\bdoes not accommodate\b",
    # "Mistakes X for necessary conditions" / "treats X as necessary"
    r"\bmistakes?\b.*\bfor (?:necessary |universal )?conditions?\b",
    r"\btreats?\b.*\bas (?:necessary|universal|essential)\b",
    # Concept genuinely applies despite failing conditions
    r"\b(?:genuinely|truly|really|plainly|clearly|manifestly|evidently|certainly|surely) (?:is|are|constitutes?)\b",
    r"\b(?:is|are|constitutes?)\b.*\b(?:genuine|legitimate|authentic|bona fide)\b.*\byet\b",
    r"\bplainly\b.*\byet the (?:definition|analysis|account)\b",
    # "Fails to recognise [that the concept can apply without X]"
    r"\bfails? to recogni[sz]e\b",
    # "History / experience shows" (empirical refutation of an allegedly necessary condition)
    r"\bthe history of\b.*\b(?:shows?|teaches?|is replete|demonstrates?)\b",
    # "Conflates X with Y" (wrong/overly specific condition)
    r"(?:the )?definition (?:conflates?|reduces?|collapses?)\b",
    # "Restricts X to Y" / "imposes" (unnecessary restriction)
    r"(?:the )?definition (?:restricts?|limits?|confines?)\b",
    r"(?:the )?definition (?:imposes?|presupposes?)\b",
    # "Grounds X solely in Y, but" / "conditions X upon Y, but"
    r"(?:the )?definition (?:grounds?|conditions?|predicates?)\b.*\bbut\b",
]

# "BOTH" signals — passages that explicitly acknowledge both directions
BOTH_PATTERNS = [
    r"\bboth too (?:broad|weak|permissive).*\band too (?:narrow|strong|restrictive)",
    r"\bboth too (?:narrow|strong|restrictive).*\band too (?:broad|weak|permissive)",
    r"\bin one direction.*\bin (?:the |an)?other direction",
    r"\btoo (?:broad|weak|permissive) in.*\btoo (?:narrow|strong|restrictive) in",
]


def compile_patterns(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


WEAK_RE = compile_patterns(TOO_WEAK_PATTERNS)
STRONG_RE = compile_patterns(TOO_STRONG_PATTERNS)
BOTH_RE = compile_patterns(BOTH_PATTERNS)


def classify_entry(entry):
    """Return (classification, weak_score, strong_score, both_score, matched_patterns)."""
    # Combine the key text fields
    text_parts = []
    for field in ["missing_condition", "passage", "counterexample", "abductive_insight"]:
        if field in entry and entry[field]:
            text_parts.append(entry[field])
    text = " ".join(text_parts)

    weak_matches = []
    strong_matches = []
    both_matches = []

    for pat in WEAK_RE:
        m = pat.search(text)
        if m:
            weak_matches.append(m.group())

    for pat in STRONG_RE:
        m = pat.search(text)
        if m:
            strong_matches.append(m.group())

    for pat in BOTH_RE:
        m = pat.search(text)
        if m:
            both_matches.append(m.group())

    weak_score = len(weak_matches)
    strong_score = len(strong_matches)
    both_score = len(both_matches)

    if both_score > 0:
        classification = "BOTH"
    elif weak_score > 0 and strong_score > 0:
        # Both signals present — look at balance
        if weak_score >= strong_score * 2:
            classification = "TOO_WEAK"
        elif strong_score >= weak_score * 2:
            classification = "TOO_STRONG"
        else:
            classification = "BOTH"
    elif weak_score > 0:
        classification = "TOO_WEAK"
    elif strong_score > 0:
        classification = "TOO_STRONG"
    else:
        classification = "AMBIGUOUS"

    return classification, weak_score, strong_score, both_score, weak_matches, strong_matches


def main():
    results = []
    by_type = defaultdict(Counter)      # defcx/abdcx → classification counts
    by_domain = defaultdict(Counter)    # domain → classification counts
    overall = Counter()

    # Collect some examples for each category
    examples = defaultdict(list)

    for cx_type in ["defcx", "abdcx"]:
        data_path = DATA_DIR / cx_type
        if not data_path.exists():
            continue
        for jsonl_file in sorted(data_path.glob("*.jsonl")):
            domain = jsonl_file.stem
            with open(jsonl_file) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    entry = json.loads(line)
                    cls, w, s, b, wm, sm = classify_entry(entry)
                    results.append({
                        "id": entry.get("id", f"{cx_type}_{domain}_{line_num}"),
                        "type": cx_type,
                        "domain": domain,
                        "subdomain": entry.get("subdomain", ""),
                        "classification": cls,
                        "weak_score": w,
                        "strong_score": s,
                    })
                    overall[cls] += 1
                    by_type[cx_type][cls] += 1
                    by_domain[domain][cls] += 1

                    # Collect up to 3 examples per category
                    if len(examples[cls]) < 3:
                        examples[cls].append({
                            "id": entry.get("id"),
                            "definition": entry.get("definition", "")[:120],
                            "missing_condition": entry.get("missing_condition", "")[:200],
                            "weak_matches": wm[:3],
                            "strong_matches": sm[:3],
                        })

    # --- Print results ---
    total = sum(overall.values())
    print("=" * 70)
    print(f"COUNTEREXAMPLE DIRECTION ANALYSIS — {total} entries")
    print("=" * 70)

    print("\n## Overall Classification\n")
    for cls in ["TOO_WEAK", "TOO_STRONG", "BOTH", "AMBIGUOUS"]:
        n = overall[cls]
        pct = 100 * n / total if total else 0
        bar = "█" * int(pct / 2)
        print(f"  {cls:<14} {n:>5}  ({pct:5.1f}%)  {bar}")

    print(f"\n  {'TOTAL':<14} {total:>5}")

    print("\n## By Entry Type\n")
    for cx_type in ["defcx", "abdcx"]:
        ct = by_type[cx_type]
        t = sum(ct.values())
        print(f"  {cx_type.upper()} ({t} entries):")
        for cls in ["TOO_WEAK", "TOO_STRONG", "BOTH", "AMBIGUOUS"]:
            n = ct[cls]
            pct = 100 * n / t if t else 0
            print(f"    {cls:<14} {n:>5}  ({pct:5.1f}%)")
        print()

    print("## By Domain\n")
    print(f"  {'Domain':<28} {'Weak':>6} {'Strong':>6} {'Both':>6} {'Ambig':>6} {'Total':>6}")
    print(f"  {'-'*28} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
    for domain in sorted(by_domain.keys()):
        ct = by_domain[domain]
        t = sum(ct.values())
        print(f"  {domain:<28} {ct['TOO_WEAK']:>6} {ct['TOO_STRONG']:>6} {ct['BOTH']:>6} {ct['AMBIGUOUS']:>6} {t:>6}")

    print("\n## Example Entries per Category\n")
    for cls in ["TOO_WEAK", "TOO_STRONG", "BOTH", "AMBIGUOUS"]:
        print(f"  --- {cls} ---")
        for ex in examples[cls]:
            print(f"  ID: {ex['id']}")
            print(f"    Def:     {ex['definition']}...")
            print(f"    Missing: {ex['missing_condition']}...")
            if ex["weak_matches"]:
                print(f"    Weak signals:   {ex['weak_matches']}")
            if ex["strong_matches"]:
                print(f"    Strong signals: {ex['strong_matches']}")
            print()

    # Write detailed results to JSON for further analysis
    out_path = DATA_DIR / "classification_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results written to {out_path}")


if __name__ == "__main__":
    main()
