#!/usr/bin/env python3
"""
Prepare the dataset for release: split by domain, generate browse files,
produce statistics.

Usage:
    python scripts/prepare_release.py
"""

import json
import os
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SFT_DIR = PROJECT_ROOT / "data" / "sft"
DEFCX_DIR = PROJECT_ROOT / "data" / "defcx"
ABDCX_DIR = PROJECT_ROOT / "data" / "abdcx"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

# How many example passages to show per domain in browse files
BROWSE_EXAMPLES_PER_DOMAIN = 5


def load_jsonl(path):
    """Load records from a JSONL file."""
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def split_by_domain(records):
    """Group records by domain."""
    by_domain = defaultdict(list)
    for rec in records:
        by_domain[rec.get("domain", "unknown")].append(rec)
    return dict(by_domain)


def write_jsonl(records, path):
    """Write records to a JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def domain_display_name(domain):
    """Convert domain slug to display name."""
    return domain.replace("_", " ").title().replace("Of ", "of ")


def generate_browse_markdown(domain, defcx_records, abdcx_records):
    """Generate a browsable markdown file for one domain."""
    name = domain_display_name(domain)
    n_defcx = len(defcx_records)
    n_abdcx = len(abdcx_records)

    lines = []
    lines.append(f"# {name}")
    lines.append("")
    lines.append(f"**{n_defcx} DefCx** + **{n_abdcx} AbdCx** = "
                 f"**{n_defcx + n_abdcx} examples**")
    lines.append("")

    # Subdomains
    subdomains = sorted(set(
        r.get("subdomain", "") for r in defcx_records + abdcx_records
    ))
    if subdomains:
        lines.append("**Subdomains:** " + ", ".join(
            s.replace("_", " ") for s in subdomains if s
        ))
        lines.append("")

    # DefCx examples
    lines.append("---")
    lines.append("")
    lines.append("## DefCx Examples")
    lines.append("")
    lines.append("Each example presents a definition as necessary and "
                 "sufficient conditions, then constructs a scenario that "
                 "reveals the definition's insufficiency.")
    lines.append("")

    for i, rec in enumerate(defcx_records[:BROWSE_EXAMPLES_PER_DOMAIN]):
        sd = rec.get("subdomain", "").replace("_", " ")
        lines.append(f"### {i+1}. {sd}")
        lines.append("")
        lines.append(f"**Definition:** {rec.get('definition', '')}")
        lines.append("")
        passage = rec.get("passage", "")
        # Preserve paragraph breaks
        for para in passage.split("\n"):
            para = para.strip()
            if para:
                lines.append(f"> {para}")
                lines.append(">")
        if lines[-1] == ">":
            lines.pop()
        lines.append("")
        mc = rec.get("missing_condition")
        if mc:
            lines.append(f"*Missing condition:* {mc}")
            lines.append("")

    if n_defcx > BROWSE_EXAMPLES_PER_DOMAIN:
        lines.append(f"*... and {n_defcx - BROWSE_EXAMPLES_PER_DOMAIN} more "
                     f"DefCx examples in "
                     f"[`data/defcx/{domain}.jsonl`](../data/defcx/{domain}.jsonl)*")
        lines.append("")

    # AbdCx examples
    if abdcx_records:
        lines.append("---")
        lines.append("")
        lines.append("## AbdCx Examples")
        lines.append("")
        lines.append("Each example presents background cases that motivate a "
                     "definition, then constructs a scenario revealing what "
                     "the background cases shared but the definition missed.")
        lines.append("")

        for i, rec in enumerate(abdcx_records[:BROWSE_EXAMPLES_PER_DOMAIN]):
            sd = rec.get("subdomain", "").replace("_", " ")
            lines.append(f"### {i+1}. {sd}")
            lines.append("")
            lines.append(f"**Definition:** {rec.get('definition', '')}")
            lines.append("")
            passage = rec.get("passage", "")
            for para in passage.split("\n"):
                para = para.strip()
                if para:
                    lines.append(f"> {para}")
                    lines.append(">")
            if lines[-1] == ">":
                lines.pop()
            lines.append("")
            ai = rec.get("abductive_insight")
            if ai:
                lines.append(f"*Abductive insight:* {ai}")
                lines.append("")

        if n_abdcx > BROWSE_EXAMPLES_PER_DOMAIN:
            lines.append(f"*... and {n_abdcx - BROWSE_EXAMPLES_PER_DOMAIN} more "
                         f"AbdCx examples in "
                         f"[`data/abdcx/{domain}.jsonl`](../data/abdcx/{domain}.jsonl)*")
            lines.append("")

    return "\n".join(lines)


def generate_examples_index(domain_stats):
    """Generate the examples/ index README."""
    lines = []
    lines.append("# Browse Examples by Domain")
    lines.append("")
    lines.append("Each file below shows a curated selection of passages from "
                 "one philosophical domain. For the full dataset, see the "
                 "JSONL files under [`data/`](../data/).")
    lines.append("")
    lines.append("| Domain | DefCx | AbdCx | Total | Browse |")
    lines.append("|--------|------:|------:|------:|--------|")

    total_defcx = 0
    total_abdcx = 0
    for domain, (nd, na) in sorted(domain_stats.items()):
        name = domain_display_name(domain)
        total = nd + na
        total_defcx += nd
        total_abdcx += na
        lines.append(f"| {name} | {nd} | {na} | {total} | "
                     f"[examples]({domain}.md) |")

    grand = total_defcx + total_abdcx
    lines.append(f"| **Total** | **{total_defcx}** | **{total_abdcx}** | "
                 f"**{grand}** | |")
    lines.append("")

    return "\n".join(lines)


def generate_data_readme(domain_stats):
    """Generate the data/ README with schema documentation."""
    lines = []
    lines.append("# Data Directory")
    lines.append("")
    lines.append("## Structure")
    lines.append("")
    lines.append("```")
    lines.append("data/")
    lines.append("├── defcx/          # Definition + Counterexample (one JSONL per domain)")
    lines.append("├── abdcx/          # Abductive Counterexample (one JSONL per domain)")
    lines.append("└── training/       # Merged, shuffled, split for model training")
    lines.append("```")
    lines.append("")

    lines.append("## DefCx Schema")
    lines.append("")
    lines.append("Each line in a DefCx JSONL file is a JSON object with:")
    lines.append("")
    lines.append("| Field | Type | Description |")
    lines.append("|-------|------|-------------|")
    lines.append("| `id` | string | Unique identifier (`defcx_{domain}_{subdomain}_{NNNN}`) |")
    lines.append("| `domain` | string | Philosophical domain |")
    lines.append("| `subdomain` | string | Specific subdomain |")
    lines.append("| `definition` | string | Proposed definition as necessary & sufficient conditions |")
    lines.append("| `conditions` | list[string] | Individual conditions (≥3) |")
    lines.append("| `counterexample` | string | Scenario where conditions hold but concept fails (2-3 sentences) |")
    lines.append("| `missing_condition` | string or null | What the definition failed to capture |")
    lines.append("| `passage` | string | Full prose passage (≥150 words) |")
    lines.append("| `source` | string | `\"manual\"` or `\"synthetic\"` |")
    lines.append("| `quality` | null | Reserved for human quality ratings |")
    lines.append("")

    lines.append("## AbdCx Schema")
    lines.append("")
    lines.append("AbdCx extends the DefCx schema with two additional fields:")
    lines.append("")
    lines.append("| Field | Type | Description |")
    lines.append("|-------|------|-------------|")
    lines.append("| `background_cases` | list[string] | 2-4 motivating cases that ground the definition |")
    lines.append("| `abductive_insight` | string | What the background cases shared that the definition missed |")
    lines.append("")
    lines.append("AbdCx passages are longer (≥200 words) and structured in two phases: "
                 "background cases → definition → counterexample → insight.")
    lines.append("")

    lines.append("## Training Format")
    lines.append("")
    lines.append("Files in `training/` contain EOT-separated passages:")
    lines.append("")
    lines.append("```")
    lines.append("<|endoftext|>")
    lines.append("[passage text]")
    lines.append("<|endoftext|>")
    lines.append("[passage text]")
    lines.append("...")
    lines.append("```")
    lines.append("")
    lines.append("Generated with a 95/5 train/val split, shuffled with seed 42.")
    lines.append("")

    return "\n".join(lines)


def main():
    # Load all data
    print("Loading data...")
    defcx_inherited = load_jsonl(SFT_DIR / "defcx_validated.jsonl")
    defcx_epist = load_jsonl(SFT_DIR / "defcx_epistemology_validated.jsonl")
    abdcx_inherited = load_jsonl(SFT_DIR / "abdcx_validated.jsonl")
    abdcx_epist = load_jsonl(SFT_DIR / "abdcx_epistemology_validated.jsonl")

    all_defcx = defcx_inherited + defcx_epist
    all_abdcx = abdcx_inherited + abdcx_epist

    print(f"  DefCx: {len(all_defcx)} ({len(defcx_inherited)} inherited + "
          f"{len(defcx_epist)} epistemology)")
    print(f"  AbdCx: {len(all_abdcx)} ({len(abdcx_inherited)} inherited + "
          f"{len(abdcx_epist)} epistemology)")
    print(f"  Total: {len(all_defcx) + len(all_abdcx)}")

    # Split by domain
    print("\nSplitting by domain...")
    defcx_by_domain = split_by_domain(all_defcx)
    abdcx_by_domain = split_by_domain(all_abdcx)
    all_domains = sorted(set(defcx_by_domain) | set(abdcx_by_domain))

    # Write per-domain JSONL files
    for domain in all_domains:
        if domain in defcx_by_domain:
            write_jsonl(defcx_by_domain[domain],
                       DEFCX_DIR / f"{domain}.jsonl")
        if domain in abdcx_by_domain:
            write_jsonl(abdcx_by_domain[domain],
                       ABDCX_DIR / f"{domain}.jsonl")
        nd = len(defcx_by_domain.get(domain, []))
        na = len(abdcx_by_domain.get(domain, []))
        print(f"  {domain}: {nd} defcx, {na} abdcx")

    # Generate browse markdown files
    print("\nGenerating browse files...")
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    domain_stats = {}

    for domain in all_domains:
        defcx_recs = defcx_by_domain.get(domain, [])
        abdcx_recs = abdcx_by_domain.get(domain, [])
        domain_stats[domain] = (len(defcx_recs), len(abdcx_recs))

        md = generate_browse_markdown(domain, defcx_recs, abdcx_recs)
        md_path = EXAMPLES_DIR / f"{domain}.md"
        with open(md_path, "w") as f:
            f.write(md)
        print(f"  {md_path.name}")

    # Examples index
    index_md = generate_examples_index(domain_stats)
    with open(EXAMPLES_DIR / "README.md", "w") as f:
        f.write(index_md)
    print("  README.md (index)")

    # Data directory README
    data_readme = generate_data_readme(domain_stats)
    data_dir = PROJECT_ROOT / "data"
    with open(data_dir / "README.md", "w") as f:
        f.write(data_readme)
    print("  data/README.md")

    # Print summary stats
    print(f"\nDataset summary:")
    print(f"  Domains: {len(all_domains)}")
    print(f"  DefCx:   {len(all_defcx)}")
    print(f"  AbdCx:   {len(all_abdcx)}")
    print(f"  Total:   {len(all_defcx) + len(all_abdcx)}")
    print(f"\nFiles written to:")
    print(f"  data/defcx/  ({len(all_domains)} JSONL files)")
    print(f"  data/abdcx/  ({len(all_domains)} JSONL files)")
    print(f"  examples/    ({len(all_domains)} browse files + index)")


if __name__ == "__main__":
    main()
