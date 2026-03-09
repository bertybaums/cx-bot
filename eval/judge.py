#!/usr/bin/env python3
"""
CX-Bot Evaluation: Tier 3 LLM-as-judge for logical quality.

Assesses whether generated counterexamples are logically sound:
  1. Condition satisfaction — do all conditions genuinely hold?
  2. Definition defeat — does the counterexample reveal insufficiency?
  3. Insight quality — is the missing_condition/abductive_insight substantive?

Modes:
  export  — write judge prompts to JSONL for manual review via Claude
  api     — call Anthropic API directly (requires ANTHROPIC_API_KEY)

Usage:
    # Export prompts for manual/CLI review
    python eval/judge.py \
        --input eval/results/scored.jsonl \
        --output eval/results/judge_prompts.jsonl \
        --mode export

    # Auto-judge via API
    python eval/judge.py \
        --input eval/results/scored.jsonl \
        --output eval/results/judged.jsonl \
        --mode api
"""

import argparse
import json
import os
import sys
from pathlib import Path


JUDGE_SYSTEM = """\
You are a philosophy examiner assessing the logical quality of \
counterexamples to proposed definitions. You evaluate whether a \
counterexample genuinely reveals a structural insufficiency in \
the definition, or whether it relies on verbal tricks, irrelevant \
scenarios, or misunderstandings of the conditions.

Score each dimension from 0 to 3:
  0 = completely fails
  1 = partially succeeds but has significant flaws
  2 = mostly succeeds with minor issues
  3 = fully succeeds

Respond with a JSON object containing:
  "condition_satisfaction": <0-3> (do all stated conditions genuinely hold in the scenario?)
  "definition_defeat": <0-3> (does the scenario reveal genuine insufficiency?)
  "insight_quality": <0-3> (is the identified gap substantive, not tautological?)
  "overall": <0-9> (sum of above)
  "reasoning": <string> (2-3 sentences explaining your assessment)"""


def build_judge_prompt(record):
    """Build the user prompt for the judge from a scored record."""
    parsed = record.get("parsed_output", {})
    task = record.get("task_type", "DefCx")

    parts = []
    parts.append(f"Task type: {task}")
    parts.append(f"Domain: {record.get('domain', '?')}, "
                 f"Subdomain: {record.get('subdomain', '?')}")
    parts.append("")

    if "definition" in parsed:
        parts.append(f"DEFINITION: {parsed['definition']}")
        parts.append("")

    if "conditions" in parsed:
        parts.append("CONDITIONS:")
        for i, c in enumerate(parsed["conditions"], 1):
            parts.append(f"  {i}. {c}")
        parts.append("")

    if task == "AbdCx" and "background_cases" in parsed:
        parts.append("BACKGROUND CASES:")
        for i, bc in enumerate(parsed["background_cases"], 1):
            parts.append(f"  {i}. {bc}")
        parts.append("")

    if "counterexample" in parsed:
        parts.append(f"COUNTEREXAMPLE: {parsed['counterexample']}")
        parts.append("")

    if task == "DefCx" and "missing_condition" in parsed:
        parts.append(f"MISSING CONDITION: {parsed['missing_condition']}")
    elif task == "AbdCx" and "abductive_insight" in parsed:
        parts.append(f"ABDUCTIVE INSIGHT: {parsed['abductive_insight']}")

    parts.append("")
    parts.append("Assess the logical quality of this counterexample.")

    return "\n".join(parts)


def export_prompts(records, output_path):
    """Write judge prompts to JSONL for manual review."""
    count = 0
    with open(output_path, "w") as f:
        for i, rec in enumerate(records):
            # Only judge records that passed Tier 1
            if not rec.get("scores", {}).get("tier1_pass", False):
                continue

            prompt = build_judge_prompt(rec)
            entry = {
                "index": i,
                "domain": rec.get("domain"),
                "subdomain": rec.get("subdomain"),
                "task_type": rec.get("task_type"),
                "judge_system": JUDGE_SYSTEM,
                "judge_prompt": prompt,
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            count += 1

    print(f"Exported {count} judge prompts to {output_path}")
    print(f"(Skipped {len(records) - count} records that failed Tier 1)")
    print(f"\nTo review manually, send each prompt to Claude with the system prompt.")


def judge_via_api(records, output_path, model="claude-sonnet-4-20250514"):
    """Score records using the Anthropic API."""
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package not installed. "
              "Install with: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()
    judged = []
    errors = 0

    eligible = [(i, r) for i, r in enumerate(records)
                if r.get("scores", {}).get("tier1_pass", False)]
    print(f"Judging {len(eligible)} records via API ({model})...")

    for idx, (i, rec) in enumerate(eligible):
        prompt = build_judge_prompt(rec)

        try:
            response = client.messages.create(
                model=model,
                max_tokens=300,
                system=JUDGE_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            raw_judge = response.content[0].text

            # Parse judge response
            try:
                judge_scores = json.loads(raw_judge)
            except json.JSONDecodeError:
                # Try extracting JSON from response
                import re
                match = re.search(r"\{[^}]+\}", raw_judge, re.DOTALL)
                if match:
                    judge_scores = json.loads(match.group())
                else:
                    judge_scores = {"error": "parse_failed", "raw": raw_judge}

            rec["judge"] = judge_scores

        except Exception as e:
            rec["judge"] = {"error": str(e)}
            errors += 1

        judged.append(rec)

        if (idx + 1) % 10 == 0:
            print(f"  [{idx+1}/{len(eligible)}]")

    # Write all records (including unjudged ones)
    with open(output_path, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Summary
    valid_judges = [r["judge"] for r in judged
                    if "error" not in r.get("judge", {})]
    if valid_judges:
        avg_cond = sum(j["condition_satisfaction"] for j in valid_judges) / len(valid_judges)
        avg_defeat = sum(j["definition_defeat"] for j in valid_judges) / len(valid_judges)
        avg_insight = sum(j["insight_quality"] for j in valid_judges) / len(valid_judges)
        avg_overall = sum(j["overall"] for j in valid_judges) / len(valid_judges)

        print(f"\nJudge Results ({len(valid_judges)} scored, {errors} errors):")
        print(f"  Condition satisfaction: {avg_cond:.2f}/3")
        print(f"  Definition defeat:     {avg_defeat:.2f}/3")
        print(f"  Insight quality:       {avg_insight:.2f}/3")
        print(f"  Overall:               {avg_overall:.2f}/9")

    print(f"\nSaved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="CX-Bot Tier 3: LLM-as-judge evaluation")
    parser.add_argument("--input", required=True,
                        help="Scored JSONL from score.py")
    parser.add_argument("--output", required=True,
                        help="Output path for judge prompts or judged results")
    parser.add_argument("--mode", choices=["export", "api"], default="export",
                        help="export: write prompts; api: call Anthropic API")
    parser.add_argument("--model", default="claude-sonnet-4-20250514",
                        help="Model for API mode")
    args = parser.parse_args()

    # Load scored records
    records = []
    with open(args.input) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loaded {len(records)} records from {args.input}")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if args.mode == "export":
        export_prompts(records, args.output)
    elif args.mode == "api":
        judge_via_api(records, args.output, model=args.model)


if __name__ == "__main__":
    main()
