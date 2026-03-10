#!/usr/bin/env python3
"""
Bias remediation for cx-bot philosophical counterexample dataset.

Automated fixes:
  1. Gender-neutralize formal fields (definition, conditions, missing_condition)
     - he/his/him/himself -> they/their/them/themselves (with verb agreement)
     - she/her/herself -> they/their/themselves (with verb agreement)
  2. Gender-rebalance narrative fields
     - ~40% of male-only entries: swap he->she, his->her, man->woman
     - Remaining: replace generic "a man who" -> "a person who"
  3. Fix disability language across all fields
     - "suffering from" -> "living with"
     - "suffers from" -> "has"
     - "afflicted with" -> "who has"
     - "crippled" -> "disabled"

Preserves logical structure, field types, and file layout.
Random seed: 42 for reproducibility.
"""

import json
import re
import random
import sys
from pathlib import Path
from copy import deepcopy

random.seed(42)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFCX_DIR = DATA_DIR / "defcx"
ABDCX_DIR = DATA_DIR / "abdcx"

SWAP_RATIO = 0.40

FORMAL_FIELDS = ["definition", "conditions", "missing_condition"]
NARRATIVE_FIELDS = ["passage", "counterexample", "background_cases",
                    "abductive_insight"]
ALL_TEXT_FIELDS = FORMAL_FIELDS + NARRATIVE_FIELDS

# Keywords indicating gender is semantically load-bearing — skip pronoun swap
SKIP_SWAP_KEYWORDS = [
    "husband", "wife", "married", "marriage", "bride", "groom",
    "widow", "widower", "pregnant", "pregnancy", "suffrage",
    "suffragette", "feminist", "king", "queen", "prince", "princess",
    "monk", "nun", "mother", "father", "son ", "daughter",
    "brother", "sister", "seamstress", "dowry", "patriarch",
    "matriarch", "brotherhood", "sisterhood", "boy ", "girl ",
    "uncle", "aunt", "nephew", "niece", "grandfather", "grandmother",
    "manhood", "womanhood", "midwife", "breastfeed",
    "his wife", "her husband", "his son", "her son",
]

# Words ending in 's' that are NOT third-person verbs (used in de-conjugation)
NOT_THIRD_PERSON_VERB = {
    "always", "sometimes", "nevertheless", "nonetheless", "perhaps",
    "thus", "afterwards", "towards", "besides", "whereas", "thereupon",
    "across", "minus", "plus", "us", "his", "its", "this",
    "is", "has", "was", "does", "goes",  # irregulars handled separately
}


# ── Helpers ──

def get_all_text(entry):
    """Concatenate all text fields for analysis."""
    parts = []
    for f in ALL_TEXT_FIELDS:
        v = entry.get(f)
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)


def has_male(text):
    return bool(re.search(r'\b(he|his|him|himself)\b', text, re.I))


def has_female(text):
    return bool(re.search(r'\b(she|her|hers|herself)\b', text, re.I))


def is_male_only(entry):
    t = get_all_text(entry)
    return has_male(t) and not has_female(t)


def should_skip_swap(entry):
    t = get_all_text(entry).lower()
    return any(kw in t for kw in SKIP_SWAP_KEYWORDS)


# ── 1. Gender-neutralize formal fields ──

def _deconj_after_they(verb):
    """De-conjugate a third-person singular verb for use after 'they'."""
    if verb.lower() in NOT_THIRD_PERSON_VERB:
        return verb  # not a verb, leave alone
    if verb.lower().endswith("ies"):
        return verb[:-3] + "y"
    if re.search(r"(sh|ch|ss|x|z)es$", verb, re.I):
        return verb[:-2]
    if verb.endswith("s"):
        return verb[:-1]
    return verb


def neutralize_he(text):
    """Replace he/his/him/himself with they/their/them/themselves,
    handling verb agreement for 'he' -> 'they'."""
    if not text or not isinstance(text, str):
        return text

    # Irregular verbs (case-sensitive pairs)
    for pat, rep in [
        (r"\bHe is\b", "They are"), (r"\bhe is\b", "they are"),
        (r"\bHe has\b", "They have"), (r"\bhe has\b", "they have"),
        (r"\bHe was\b", "They were"), (r"\bhe was\b", "they were"),
        (r"\bHe does\b", "They do"), (r"\bhe does\b", "they do"),
        (r"\bHe goes\b", "They go"), (r"\bhe goes\b", "they go"),
    ]:
        text = re.sub(pat, rep, text)

    # Regular "he [verb]s" -> "they [verb]"
    def _deconj_he(m):
        he_word, verb = m.group(1), m.group(2)
        prefix = "They" if he_word[0].isupper() else "they"
        return prefix + " " + _deconj_after_they(verb)

    text = re.sub(r"\b(He|he) (\w+s)\b", _deconj_he, text)

    # Remaining standalone "he" (before modals, past tense, etc.)
    text = re.sub(r"\bHe\b", "They", text)
    text = re.sub(r"\bhe\b", "they", text)

    # Possessives and objects
    text = re.sub(r"\bHimself\b", "Themselves", text)
    text = re.sub(r"\bhimself\b", "themselves", text)
    text = re.sub(r"\bHis\b", "Their", text)
    text = re.sub(r"\bhis\b", "their", text)
    text = re.sub(r"\bHim\b", "Them", text)
    text = re.sub(r"\bhim\b", "them", text)

    return text


def neutralize_she(text):
    """Replace she/her/herself with they/their/themselves,
    handling verb agreement for 'she' -> 'they'."""
    if not text or not isinstance(text, str):
        return text

    # Irregular verbs
    for pat, rep in [
        (r"\bShe is\b", "They are"), (r"\bshe is\b", "they are"),
        (r"\bShe has\b", "They have"), (r"\bshe has\b", "they have"),
        (r"\bShe was\b", "They were"), (r"\bshe was\b", "they were"),
        (r"\bShe does\b", "They do"), (r"\bshe does\b", "they do"),
    ]:
        text = re.sub(pat, rep, text)

    # Regular "she [verb]s" -> "they [verb]"
    def _deconj_she(m):
        she_word, verb = m.group(1), m.group(2)
        prefix = "They" if she_word[0].isupper() else "they"
        return prefix + " " + _deconj_after_they(verb)

    text = re.sub(r"\b(She|she) (\w+s)\b", _deconj_she, text)

    # Remaining standalone "she"
    text = re.sub(r"\bShe\b", "They", text)
    text = re.sub(r"\bshe\b", "they", text)

    # herself -> themselves
    text = re.sub(r"\bHerself\b", "Themselves", text)
    text = re.sub(r"\bherself\b", "themselves", text)

    # "her" is ambiguous: possessive (her X) vs object (to her)
    # Handle object cases first (after prepositions / at clause end)
    text = re.sub(
        r"\b(to|for|from|with|by|upon|about|against|between|toward|towards|"
        r"of|give|tell|inform|offer|allow|permit|enable|require|oblige|"
        r"compel|cause|cost|deny|grant|owe|assign|before|after|beyond|"
        r"without|within|under|over|around|through|near|beside|behind|"
        r"inside|outside|beneath|above|among|except) her\b",
        lambda m: m.group(1) + " them", text, flags=re.I)
    # Now "her [word]" is possessive -> their
    text = re.sub(r"\bHer (\w)", lambda m: "Their " + m.group(1), text)
    text = re.sub(r"\bher (\w)", lambda m: "their " + m.group(1), text)
    # Any remaining "her" (e.g. end of sentence) -> them
    text = re.sub(r"\bHer\b", "Them", text)
    text = re.sub(r"\bher\b", "them", text)

    return text


def neutralize_formal(text):
    """Neutralize all gendered pronouns in formal text."""
    text = neutralize_he(text)
    text = neutralize_she(text)
    return text


def neutralize_field(value):
    """Apply neutralization to a field value (string or list)."""
    if isinstance(value, str):
        return neutralize_formal(value)
    elif isinstance(value, list):
        return [neutralize_formal(x) if isinstance(x, str) else x
                for x in value]
    return value


# ── 2. Swap male -> female in narrative fields ──

def swap_to_female(text):
    """Swap male pronouns/nouns to female equivalents."""
    if not text or not isinstance(text, str):
        return text

    for pat, rep in [
        (r"\bHimself\b", "Herself"), (r"\bhimself\b", "herself"),
        (r"\bHis\b", "Her"), (r"\bhis\b", "her"),
        (r"\bHim\b", "Her"), (r"\bhim\b", "her"),
        (r"\bHe\b", "She"), (r"\bhe\b", "she"),
        # Nouns with articles/demonstratives
        (r"\bA man\b", "A woman"), (r"\ba man\b", "a woman"),
        (r"\bThe man\b", "The woman"), (r"\bthe man\b", "the woman"),
        (r"\bThis man\b", "This woman"), (r"\bthis man\b", "this woman"),
        (r"\bThat man\b", "That woman"), (r"\bthat man\b", "that woman"),
        (r"\ba young man\b", "a young woman"),
        (r"\bA young man\b", "A young woman"),
        (r"\bthe young man\b", "the young woman"),
        (r"\ba wise man\b", "a wise woman"),
        (r"\ba reasonable man\b", "a reasonable woman"),
        # Plural
        (r"\bmen\b", "women"), (r"\bMen\b", "Women"),
        # Titles
        (r"\bMr\.\s", "Ms. "),
        # Misc
        (r"\bgentleman\b", "gentlewoman"),
    ]:
        text = re.sub(pat, rep, text)

    return text


def swap_field(value):
    """Apply gender swap to a field (string or list)."""
    if isinstance(value, str):
        return swap_to_female(value)
    elif isinstance(value, list):
        return [swap_to_female(x) if isinstance(x, str) else x
                for x in value]
    return value


# ── 3. Disability language ──

def fix_disability(text):
    """Replace stigmatizing disability language with neutral alternatives."""
    if not text or not isinstance(text, str):
        return text

    # Order matters: more specific patterns first
    text = re.sub(r"\bis afflicted with\b", "has", text, flags=re.I)
    text = re.sub(r"\bafflicted with\b", "who has", text, flags=re.I)
    text = re.sub(r"\bsuffering from\b", "living with", text, flags=re.I)
    text = re.sub(r"\bsuffers from\b", "has", text, flags=re.I)
    text = re.sub(r"\bcrippled\b", "disabled", text, flags=re.I)

    # Fix capitalization after case-insensitive replacement
    text = re.sub(r"(?<=\. )living with", "Living with", text)
    text = re.sub(r"(?<=\. )who has", "Who has", text)
    text = re.sub(r"^living with", "Living with", text)
    text = re.sub(r"^who has", "Who has", text)

    return text


def fix_disability_field(value):
    if isinstance(value, str):
        return fix_disability(value)
    elif isinstance(value, list):
        return [fix_disability(x) if isinstance(x, str) else x
                for x in value]
    return value


# ── 4. Generic "a man" -> "a person" ──

def genericize_man(text):
    """Replace generic 'a man who' with 'a person who' in non-swapped entries."""
    if not text or not isinstance(text, str):
        return text

    for pat, rep in [
        (r"\ba man who\b", "a person who"),
        (r"\bA man who\b", "A person who"),
        (r"\ba man of\b", "a person of"),
        (r"\bA man of\b", "A person of"),
        (r"\bthe man of\b", "the person of"),
        (r"\bThe man of\b", "The person of"),
    ]:
        text = re.sub(pat, rep, text)
    return text


def genericize_field(value):
    if isinstance(value, str):
        return genericize_man(value)
    elif isinstance(value, list):
        return [genericize_man(x) if isinstance(x, str) else x
                for x in value]
    return value


# ── Main processing ──

def process_entry(entry, swap_gender=False):
    """Process a single entry with all applicable fixes."""
    entry = deepcopy(entry)

    # 1. Neutralize ALL formal fields (definition, conditions, missing_condition)
    for f in FORMAL_FIELDS:
        if f in entry:
            entry[f] = neutralize_field(entry[f])

    # 2. Narrative fields: either swap or genericize
    if swap_gender:
        for f in NARRATIVE_FIELDS:
            if f in entry:
                entry[f] = swap_field(entry[f])
    else:
        for f in NARRATIVE_FIELDS:
            if f in entry:
                entry[f] = genericize_field(entry[f])

    # 3. Disability language in ALL fields
    for f in ALL_TEXT_FIELDS:
        if f in entry:
            entry[f] = fix_disability_field(entry[f])

    return entry


def process_file(filepath):
    """Process a JSONL file. Returns (processed_entries, stats)."""
    entries = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    # Identify male-only entries eligible for gender swap
    eligible = [i for i, e in enumerate(entries)
                if is_male_only(e) and not should_skip_swap(e)]

    # Select ~40% for swap
    n_swap = round(len(eligible) * SWAP_RATIO)
    swap_indices = set(random.sample(eligible, min(n_swap, len(eligible))))

    processed = []
    stats = {"total": len(entries), "swapped": 0, "eligible": len(eligible)}

    for i, entry in enumerate(entries):
        do_swap = i in swap_indices
        new_entry = process_entry(entry, swap_gender=do_swap)
        if do_swap:
            stats["swapped"] += 1
        processed.append(new_entry)

    return processed, stats


def write_jsonl(filepath, entries):
    with open(filepath, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    total = {"entries": 0, "swapped": 0, "eligible": 0, "files": 0}

    for directory in [DEFCX_DIR, ABDCX_DIR]:
        for filepath in sorted(directory.glob("*.jsonl")):
            entries, stats = process_file(filepath)
            write_jsonl(filepath, entries)

            total["entries"] += stats["total"]
            total["swapped"] += stats["swapped"]
            total["eligible"] += stats["eligible"]
            total["files"] += 1

            rel = filepath.relative_to(DATA_DIR)
            print(f"  {rel}: {stats['total']} entries, "
                  f"{stats['eligible']} eligible, "
                  f"{stats['swapped']} swapped")

    print(f"\nTotal: {total['entries']} entries in {total['files']} files")
    print(f"Male-only eligible: {total['eligible']}")
    print(f"Gender-swapped to female: {total['swapped']}")
    print(f"Swap ratio achieved: {total['swapped']/max(total['eligible'],1):.1%}")


if __name__ == "__main__":
    main()
