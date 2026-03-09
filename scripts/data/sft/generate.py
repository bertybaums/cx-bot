#!/usr/bin/env python3
"""
Batch generation of SFT examples for DefCx and AbdCx datasets.

Generalised from the gettier project — supports all domains including
epistemology. No domain-specific exclusion filters.

Two modes:
  --mode api     Generate examples via Anthropic API (requires ANTHROPIC_API_KEY)
  --mode manual  Import hand-written examples from a JSONL file

Usage:
    # API generation
    python scripts/data/sft/generate.py --mode api \
        --dataset defcx --domain epistemology --n 50 \
        --output data/sft/defcx_epistemology.jsonl

    # Generate for all domains
    python scripts/data/sft/generate.py --mode api \
        --dataset defcx --all-domains \
        --output data/sft/defcx.jsonl

    # Manual input
    python scripts/data/sft/generate.py --mode manual \
        --input my_examples.jsonl --output data/sft/defcx.jsonl
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.data.sft.domains import (
    DOMAINS,
    REGISTER_GUIDELINES,
    get_domain_by_name,
)


# ── Generation prompts ──

DEFCX_SYSTEM_PROMPT = f"""\
You are a philosopher writing for an analytic philosophy journal in the \
period 1920-1960. You produce passages that examine definitions of concepts \
by constructing cases that reveal their insufficiency.

{REGISTER_GUIDELINES}

You will be given a domain and subdomain. For each example, you must:
1. Choose a specific concept within the given domain and subdomain.
2. Formulate a plausible definition as necessary and jointly sufficient \
conditions (at least 3 conditions).
3. Construct a specific counterexample scenario where all conditions are met \
but the concept nevertheless fails to apply.
4. The counterexample must be non-trivial — not a trick of verbal ambiguity \
but a genuine structural gap in the definition.
5. Optionally, identify the missing condition that would repair the definition.
6. Write the result as a single continuous prose passage.

Return your output as a JSON object with these fields:
- "domain": the domain name
- "subdomain": the subdomain name
- "definition": the definition being examined (one sentence)
- "conditions": a list of the individual conditions (strings)
- "counterexample": the counterexample scenario (2-3 sentences)
- "missing_condition": what the definition failed to capture (one sentence, \
or null)
- "passage": the full prose passage (one or more paragraphs, at least 150 \
words)
"""

ABDCX_SYSTEM_PROMPT = f"""\
You are a philosopher writing for an analytic philosophy journal in the \
period 1920-1960. You produce passages that examine definitions of concepts \
by first presenting background cases that motivate the definition, then \
constructing a case that reveals how the definition fails to capture what \
the background cases had in common.

{REGISTER_GUIDELINES}

You will be given a domain and subdomain. For each example, you must:
1. Present 2-4 background cases/examples that motivate a definition.
2. Extract a definition from those cases as necessary and jointly sufficient \
conditions (at least 3 conditions).
3. Construct a counterexample that exploits a feature the background cases \
shared but the definition failed to capture.
4. Articulate the abductive insight — what the background cases had in common \
that got lost in the abstraction.
5. The counterexample must be non-trivial — a genuine structural gap, not \
verbal trickery.
6. Write the result as continuous prose (two or more paragraphs).

Return your output as a JSON object with these fields:
- "domain": the domain name
- "subdomain": the subdomain name
- "background_cases": a list of 2-4 case descriptions (strings)
- "definition": the definition extracted from the cases (one sentence)
- "conditions": a list of the individual conditions (strings)
- "counterexample": the counterexample scenario (2-3 sentences)
- "abductive_insight": what the background cases shared that the definition \
dropped (1-2 sentences)
- "passage": the full prose passage (two or more paragraphs, at least 200 \
words)
"""

DEFCX_USER_TEMPLATE = """\
Generate {n} distinct DefCx examples for the domain "{domain}", \
subdomain "{subdomain}".

Each example should examine a different concept or a different definition \
of the same concept. Return a JSON array of {n} objects.
"""

ABDCX_USER_TEMPLATE = """\
Generate {n} distinct AbdCx examples for the domain "{domain}", \
subdomain "{subdomain}".

Each example should examine a different concept or a different definition \
of the same concept. Return a JSON array of {n} objects.
"""


def load_existing_ids(output_path):
    """Load IDs already present in the output file for resumability."""
    ids = set()
    if output_path.exists():
        with open(output_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rec = json.loads(line)
                        ids.add(rec.get("id", ""))
                    except json.JSONDecodeError:
                        continue
    return ids


def make_id(dataset, domain, subdomain, index):
    """Generate a deterministic example ID."""
    return f"{dataset}_{domain}_{subdomain}_{index:04d}"


def generate_batch_api(dataset, domain_name, subdomain, n, batch_size=10):
    """Generate examples via Anthropic API.

    Returns list of dicts. Requires anthropic package and ANTHROPIC_API_KEY.
    """
    try:
        import anthropic
    except ImportError:
        print("Error: 'anthropic' package required for API mode.")
        print("Install with: pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic()

    if dataset == "defcx":
        system_prompt = DEFCX_SYSTEM_PROMPT
        user_template = DEFCX_USER_TEMPLATE
    else:
        system_prompt = ABDCX_SYSTEM_PROMPT
        user_template = ABDCX_USER_TEMPLATE

    all_examples = []
    remaining = n
    batch_idx = 0
    max_retries = 3

    while remaining > 0:
        batch_n = min(remaining, batch_size)
        user_msg = user_template.format(
            n=batch_n, domain=domain_name, subdomain=subdomain,
        )

        print(f"  Requesting {batch_n} examples "
              f"({domain_name}/{subdomain}, batch {batch_idx})...")

        retries = 0
        response = None
        while retries < max_retries:
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=8192,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_msg}],
                )
                break
            except Exception as e:
                retries += 1
                print(f"  API error (attempt {retries}/{max_retries}): {e}")
                if retries < max_retries:
                    print("  Waiting 30s before retry...")
                    time.sleep(30)

        if response is None:
            print(f"  Skipping {domain_name}/{subdomain} batch {batch_idx} "
                  f"after {max_retries} failures.")
            break

        # Extract JSON from response
        text = response.content[0].text
        examples = _parse_json_response(text)

        if not examples:
            print(f"  Warning: failed to parse response for "
                  f"{domain_name}/{subdomain} batch {batch_idx}")
            batch_idx += 1
            continue

        # Annotate with metadata
        for i, ex in enumerate(examples):
            ex["id"] = make_id(dataset, domain_name, subdomain,
                               batch_idx * batch_size + i)
            ex["source"] = "synthetic"
            ex["quality"] = None
            ex.setdefault("domain", domain_name)
            ex.setdefault("subdomain", subdomain)

        all_examples.extend(examples)
        remaining -= len(examples)
        batch_idx += 1

        # Rate limiting
        if remaining > 0:
            time.sleep(2)

    return all_examples


def _parse_json_response(text):
    """Extract a JSON array from an API response, handling markdown fences."""
    text = text.strip()

    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last fence lines
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # Try parsing as JSON array
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            return [result]
    except json.JSONDecodeError:
        pass

    # Try to find a JSON array in the text
    bracket_start = text.find("[")
    bracket_end = text.rfind("]")
    if bracket_start >= 0 and bracket_end > bracket_start:
        try:
            return json.loads(text[bracket_start:bracket_end + 1])
        except json.JSONDecodeError:
            pass

    return []


def append_examples(examples, output_path, existing_ids):
    """Append new examples to output JSONL, skipping duplicates."""
    added = 0
    with open(output_path, "a") as f:
        for ex in examples:
            ex_id = ex.get("id", "")
            if ex_id in existing_ids:
                continue
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
            existing_ids.add(ex_id)
            added += 1
    return added


def mode_api(args):
    """Run API generation mode."""
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    existing_ids = load_existing_ids(output_path)
    print(f"Existing examples in {output_path}: {len(existing_ids)}")

    if args.all_domains:
        # Generate for all domains, distributing n proportionally
        for domain in DOMAINS:
            domain_name = domain["name"]
            target_key = f"{args.dataset}_target"
            domain_target = domain.get(target_key, 0)
            if domain_target == 0:
                continue

            # Count existing for this domain
            domain_existing = sum(
                1 for eid in existing_ids if eid.startswith(
                    f"{args.dataset}_{domain_name}_"
                )
            )
            domain_remaining = domain_target - domain_existing
            if domain_remaining <= 0:
                print(f"Skipping {domain_name}: "
                      f"already have {domain_existing}/{domain_target}")
                continue

            # Distribute across subdomains
            per_subdomain = max(1, domain_remaining // len(domain["subdomains"]))
            for subdomain in domain["subdomains"]:
                sub_existing = sum(
                    1 for eid in existing_ids if eid.startswith(
                        f"{args.dataset}_{domain_name}_{subdomain}_"
                    )
                )
                sub_n = per_subdomain - sub_existing
                if sub_n <= 0:
                    continue

                examples = generate_batch_api(
                    args.dataset, domain_name, subdomain, sub_n,
                )
                added = append_examples(examples, output_path, existing_ids)
                print(f"  Added {added} examples for "
                      f"{domain_name}/{subdomain}")
    else:
        # Single domain
        if not args.domain:
            print("Error: --domain required unless --all-domains is set.")
            sys.exit(1)

        domain = get_domain_by_name(args.domain)
        if not domain:
            print(f"Error: unknown domain '{args.domain}'")
            sys.exit(1)

        subdomain = args.subdomain
        if subdomain:
            subdomains = [subdomain]
        else:
            subdomains = domain["subdomains"]

        per_subdomain = max(1, args.n // len(subdomains))
        for sd in subdomains:
            examples = generate_batch_api(
                args.dataset, args.domain, sd, per_subdomain,
            )
            added = append_examples(examples, output_path, existing_ids)
            print(f"  Added {added} examples for {args.domain}/{sd}")

    total = len(load_existing_ids(output_path))
    print(f"\nTotal examples in {output_path}: {total}")


def mode_manual(args):
    """Import hand-written examples from a JSONL file."""
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    existing_ids = load_existing_ids(output_path)

    examples = []
    with open(input_path) as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                rec.setdefault("source", "manual")
                rec.setdefault("quality", None)
                examples.append(rec)
            except json.JSONDecodeError as e:
                print(f"Warning: invalid JSON on line {line_no}: {e}")

    added = append_examples(examples, output_path, existing_ids)
    print(f"Imported {added} examples from {input_path}")
    print(f"Total examples in {output_path}: {len(existing_ids)}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SFT examples for DefCx/AbdCx datasets")
    parser.add_argument(
        "--mode", required=True, choices=["api", "manual"],
        help="Generation mode: 'api' for Anthropic API, 'manual' for import")
    parser.add_argument(
        "--dataset", choices=["defcx", "abdcx"],
        help="Which dataset to generate (required for api mode)")
    parser.add_argument(
        "--domain", default=None,
        help="Domain to generate for (api mode)")
    parser.add_argument(
        "--subdomain", default=None,
        help="Specific subdomain (api mode, optional)")
    parser.add_argument(
        "--all-domains", action="store_true",
        help="Generate for all domains (api mode)")
    parser.add_argument(
        "--n", type=int, default=50,
        help="Number of examples to generate per domain (api mode)")
    parser.add_argument(
        "--input", default=None,
        help="Input JSONL file (manual mode)")
    parser.add_argument(
        "--output", required=True,
        help="Output JSONL file path")

    args = parser.parse_args()

    if args.mode == "api":
        if not args.dataset:
            parser.error("--dataset required for api mode")
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("Error: ANTHROPIC_API_KEY environment variable not set.")
            sys.exit(1)
        mode_api(args)
    else:
        if not args.input:
            parser.error("--input required for manual mode")
        mode_manual(args)


if __name__ == "__main__":
    main()
