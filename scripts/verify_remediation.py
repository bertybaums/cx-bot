#!/usr/bin/env python3
"""
Post-remediation verification for cx-bot dataset.

Checks for:
  1. Verb agreement errors after he->they replacement ("they acts", etc.)
  2. Remaining gendered pronouns in formal fields
  3. Remaining disability language
  4. JSON validity and field preservation
  5. Gender balance statistics
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFCX_DIR = DATA_DIR / "defcx"
ABDCX_DIR = DATA_DIR / "abdcx"

FORMAL_FIELDS = ["definition", "conditions", "missing_condition"]
NARRATIVE_FIELDS = ["passage", "counterexample", "background_cases",
                    "abductive_insight"]
ALL_TEXT_FIELDS = FORMAL_FIELDS + NARRATIVE_FIELDS

# Common third-person-singular verbs that signal agreement errors after "they"
THIRD_PERSON_VERBS = [
    "acts", "appears", "applies", "arises", "asks", "asserts",
    "bears", "becomes", "begins", "believes", "belongs", "brings",
    "calls", "carries", "causes", "claims", "comes", "commits",
    "concerns", "considers", "consists", "constitutes", "contains",
    "contributes", "creates",
    "decides", "declares", "defines", "demands", "denies",
    "depends", "describes", "determines", "directs", "discovers",
    "displays", "distinguishes",
    "employs", "entails", "enters", "establishes", "examines",
    "exceeds", "exercises", "exists", "expects", "experiences",
    "expresses", "extends",
    "faces", "fails", "falls", "feels", "finds", "follows",
    "forms", "fulfils", "functions",
    "generates", "gets", "gives", "governs", "grants", "grasps",
    "holds", "identifies", "implies", "includes", "indicates",
    "intends", "involves", "issues",
    "judges", "justifies", "keeps", "knows",
    "lacks", "leads", "leaves", "lies", "lives", "looks", "loses",
    "maintains", "makes", "manifests", "means", "meets", "moves",
    "needs", "notes", "observes", "obtains", "occurs", "offers",
    "operates", "orders", "owns",
    "passes", "pays", "performs", "permits", "places", "plays",
    "points", "possesses", "presents", "preserves", "presumes",
    "prevents", "produces", "proposes", "proves", "provides",
    "pursues", "puts",
    "raises", "reaches", "reads", "receives", "recognises",
    "recognizes", "refers", "reflects", "regards", "relates",
    "remains", "removes", "renders", "represents", "requires",
    "resembles", "rests", "results", "retains", "returns",
    "reveals", "runs",
    "satisfies", "says", "seeks", "seems", "serves", "sets",
    "shows", "speaks", "stands", "states", "strikes", "suggests",
    "supports", "supposes", "takes", "tells", "thinks", "turns",
    "understands", "uses", "violates", "wants", "wishes", "works",
    "writes", "yields",
]


def get_text(entry, fields):
    """Extract text from specified fields."""
    parts = []
    for f in fields:
        v = entry.get(f)
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)


def check_verb_agreement(text, entry_id):
    """Find 'they [third-person-verb]' patterns that suggest agreement errors."""
    issues = []
    for verb in THIRD_PERSON_VERBS:
        pattern = r"\bthey " + re.escape(verb) + r"\b"
        if re.search(pattern, text, re.I):
            issues.append(f"  {entry_id}: 'they {verb}' (verb agreement)")
    return issues


def check_formal_pronouns(entry):
    """Check for remaining gendered pronouns in formal fields."""
    issues = []
    text = get_text(entry, FORMAL_FIELDS)
    eid = entry.get("id", "?")

    for pron in ["he", "his", "him", "himself", "she", "her", "herself"]:
        if re.search(r"\b" + pron + r"\b", text, re.I):
            issues.append(f"  {eid}: '{pron}' in formal field")
    return issues


def check_disability_language(entry):
    """Check for remaining stigmatizing disability language."""
    issues = []
    text = get_text(entry, ALL_TEXT_FIELDS)
    eid = entry.get("id", "?")

    for pat in [r"\bsuffering from\b", r"\bsuffers from\b",
                r"\bafflicted with\b", r"\bcrippled\b"]:
        if re.search(pat, text, re.I):
            issues.append(f"  {eid}: remaining '{pat}' in text")
    return issues


def count_pronouns(text):
    """Count male and female pronouns."""
    male = len(re.findall(r"\b(he|his|him|himself)\b", text, re.I))
    female = len(re.findall(r"\b(she|her|hers|herself)\b", text, re.I))
    return male, female


def main():
    verb_issues = []
    formal_issues = []
    disability_issues = []
    total_male = total_female = 0
    total_entries = 0
    invalid_json = 0

    for directory in [DEFCX_DIR, ABDCX_DIR]:
        for filepath in sorted(directory.glob("*.jsonl")):
            with open(filepath) as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        invalid_json += 1
                        print(f"INVALID JSON: {filepath}:{lineno}")
                        continue

                    total_entries += 1
                    eid = entry.get("id", f"{filepath.name}:{lineno}")
                    all_text = get_text(entry, ALL_TEXT_FIELDS)

                    # Verb agreement in formal fields
                    formal_text = get_text(entry, FORMAL_FIELDS)
                    verb_issues.extend(check_verb_agreement(formal_text, eid))

                    # Gendered pronouns in formal fields
                    formal_issues.extend(check_formal_pronouns(entry))

                    # Disability language
                    disability_issues.extend(check_disability_language(entry))

                    # Pronoun balance (narrative fields only)
                    narr_text = get_text(entry, NARRATIVE_FIELDS)
                    m, f_ = count_pronouns(narr_text)
                    total_male += m
                    total_female += f_

    # Report
    print(f"=== VERIFICATION REPORT ===\n")
    print(f"Total entries: {total_entries}")
    print(f"Invalid JSON: {invalid_json}\n")

    print(f"--- Verb agreement issues in formal fields ---")
    if verb_issues:
        # Deduplicate similar patterns
        seen = set()
        unique = []
        for issue in verb_issues:
            key = issue.split("'")[1] if "'" in issue else issue
            if key not in seen:
                seen.add(key)
                unique.append(issue)
        for issue in unique[:50]:
            print(issue)
        if len(unique) > 50:
            print(f"  ... and {len(unique) - 50} more")
        print(f"  Total: {len(verb_issues)} issues ({len(unique)} unique patterns)")
    else:
        print("  None found")

    print(f"\n--- Gendered pronouns remaining in formal fields ---")
    if formal_issues:
        # Count by pronoun
        pron_counts = Counter()
        for issue in formal_issues:
            pron = re.search(r"'(\w+)'", issue)
            if pron:
                pron_counts[pron.group(1)] += 1
        for pron, count in pron_counts.most_common():
            print(f"  '{pron}': {count} entries")
        print(f"  Total: {len(formal_issues)} issues")
        # Show first 10 examples
        for issue in formal_issues[:10]:
            print(issue)
    else:
        print("  None found")

    print(f"\n--- Disability language remaining ---")
    if disability_issues:
        for issue in disability_issues[:20]:
            print(issue)
        print(f"  Total: {len(disability_issues)} issues")
    else:
        print("  None found")

    print(f"\n--- Gender balance (narrative fields) ---")
    total_pron = total_male + total_female
    if total_pron > 0:
        print(f"  Male pronouns: {total_male} ({total_male/total_pron:.1%})")
        print(f"  Female pronouns: {total_female} ({total_female/total_pron:.1%})")
        print(f"  Ratio: {total_male/max(total_female,1):.2f}:1")
    else:
        print("  No gendered pronouns found")

    # Exit code: 0 if no critical issues
    n_critical = invalid_json + len(verb_issues)
    if n_critical > 0:
        print(f"\n{n_critical} issues need attention.")
        return 1
    else:
        print(f"\nAll checks passed.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
