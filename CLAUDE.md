# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A general-purpose counterexample (CX) corpus for training language models to recognise and generate philosophical counterexamples — cases that reveal the insufficiency of proposed definitions stated as necessary and sufficient conditions.

Generalised from the `gettier` project (sibling directory), which deliberately excluded epistemology to keep its evaluation clean. This project **includes epistemology** alongside all 14 other domains.

## Relation to gettier project

The gettier project (`../_RCDS/gettier/`) built a corpus of ~4,100 counterexamples across 14 philosophical domains, intentionally filtering out all epistemological content. This project inherits that corpus verbatim and extends it with epistemology examples — the domain most naturally rich in counterexamples to definitions, given the cottage industry of papers following Gettier (1963).

## Data

### SFT examples (`data/sft/`)

Two complementary formats:

**DefCx** (Definition + Counterexample):
- Fields: `id`, `domain`, `subdomain`, `definition`, `conditions`, `counterexample`, `missing_condition`, `passage`
- A definition is stated as necessary and sufficient conditions; a scenario is constructed where all conditions hold but the concept fails to apply

**AbdCx** (Abductive Counterexample):
- Fields: all DefCx fields plus `background_cases`, `abductive_insight`
- Background cases motivate a definition; the counterexample exploits a feature the cases shared but the definition dropped

### Inherited corpus (from gettier)

- 3,026 validated DefCx examples across 14 domains
- 1,113 validated AbdCx examples across 14 domains
- All non-epistemological (ethics, aesthetics, logic, mathematics, law, etc.)

### New epistemology domain

Target: ~250 DefCx + ~85 AbdCx (proportional to other domains)

Subdomains: knowledge, justification, belief, perception, testimony, memory_epistemic, a_priori, skepticism, truth, epistemic_virtue

## Scripts

All in `scripts/data/sft/`:

- `domains.py` — Domain definitions (15 domains), register guidelines. Pure data module.
- `generate.py` — Batch generation via Anthropic API or manual import
- `validate.py` — Structural validation, condition overlap check, TF-IDF deduplication
- `format_sft.py` — Convert validated JSONL to EOT-separated plain text for training

### Typical workflow

```bash
# Generate epistemology DefCx examples
python scripts/data/sft/generate.py --mode api \
    --dataset defcx --domain epistemology --n 250 \
    --output data/sft/defcx_epistemology.jsonl

# Validate
python scripts/data/sft/validate.py \
    --input data/sft/defcx_epistemology.jsonl \
    --output data/sft/defcx_epistemology_validated.jsonl \
    --report data/sft/defcx_epistemology_report.txt

# Merge and format for training
python scripts/data/sft/format_sft.py \
    --input data/sft/defcx_validated.jsonl data/sft/defcx_epistemology_validated.jsonl \
           data/sft/abdcx_validated.jsonl data/sft/abdcx_epistemology_validated.jsonl \
    --output-prefix data/sft/combined \
    --shuffle --split 0.95
```

## Register

All passages are written in the style of early-to-mid twentieth-century analytic philosophy (Russell, Moore, Ayer, Broad, Ryle): continuous prose, British spelling, hedging language, no modern jargon or formatting. See `REGISTER_GUIDELINES` in `domains.py`.

## Domain targets

| Domain | DefCx | AbdCx |
|--------|-------|-------|
| ethics | 300 | 100 |
| mathematics | 300 | 100 |
| philosophy_of_mind | 250 | 100 |
| **epistemology** | **250** | **85** |
| law | 250 | 100 |
| aesthetics | 200 | 80 |
| political_philosophy | 200 | 80 |
| philosophy_of_language | 200 | 70 |
| natural_science | 200 | 80 |
| logic | 200 | 70 |
| metaphysics | 180 | 65 |
| philosophy_of_science | 150 | 55 |
| everyday_concepts | 150 | 50 |
| philosophy_of_religion | 130 | 50 |
| social_philosophy | 130 | 50 |
| philosophy_of_history | 120 | 45 |
