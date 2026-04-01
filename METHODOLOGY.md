# Methodology

## Overview
This dataset contains 4,474 philosophical counterexamples across 16 domains. Each example presents a definition of a concept stated as necessary and sufficient conditions, then constructs a scenario that reveals the definition's structural insufficiency. The dataset is designed for training language models to recognise and generate this core philosophical skill.

## Two Complementary Formats

### DefCx (Definition + Counterexample)
- 3,276 examples
- A definition is stated as necessary and jointly sufficient conditions (≥3 conditions)
- A counterexample scenario is constructed where all conditions hold but the concept fails to apply (or vice versa)
- Optionally identifies the missing condition that would repair the definition
- Passage: ≥150 words of continuous prose

### AbdCx (Abductive Counterexample)
- 1,198 examples
- Extends DefCx with an abductive reasoning step
- 2-4 background cases motivate the definition
- The counterexample exploits a feature the background cases shared but the definition failed to capture
- An abductive insight articulates what was lost in the abstraction
- Passage: ≥200 words of continuous prose

## Domain Coverage
16 philosophical domains: aesthetics, epistemology, ethics, everyday concepts, law, logic, mathematics, metaphysics, natural science, philosophy of history, philosophy of language, philosophy of mind, philosophy of religion, philosophy of science, political philosophy, social philosophy.

Each domain contains multiple subdomains (e.g., epistemology has: knowledge, justification, belief, perception, testimony, memory, a priori, skepticism, truth, epistemic virtue).

## Provenance
The dataset was generated in two phases:
1. **Phase 1 (14 domains):** Originally created for a research project studying whether an LLM trained exclusively on pre-1963 philosophy could independently generate Gettier-style counterexamples. Epistemology was deliberately excluded from this phase to keep the evaluation uncontaminated.
2. **Phase 2 (epistemology):** 335 epistemology examples (250 DefCx + 85 AbdCx) were added, drawing on the rich post-Gettier literature on knowledge, justification, and related concepts.

## Generation Process
Examples were generated using Claude (Anthropic) within Claude Code sessions. Each example was produced by prompting with:
- A target domain and subdomain
- The DefCx or AbdCx schema
- Register guidelines enforcing early-to-mid 20th century analytic philosophy style
- Explicit instructions for structural quality (≥3 conditions, non-trivial counterexamples, no verbal trickery)

### Register Guidelines
All passages are written in the style of early-to-mid twentieth-century analytic philosophy (Russell, Moore, Ayer, Broad, Ryle):
- Continuous prose paragraphs (no bullets, numbered lists, or section headers)
- Hedging language ("one might observe," "it appears," "we should hesitate to say")
- British spelling (analyse, defence, behaviour, recognise)
- Impersonal or first-person plural voice
- Period-appropriate vocabulary and phrasing (1920-1960)
- The word "counterexample" is avoided; instead: "a case which reveals the insufficiency of this analysis"

## Validation Pipeline
Every example passes through a structural validation pipeline (`scripts/data/sft/validate.py`):

### Structural Checks
- All required fields present
- `conditions` is a list of ≥2 strings (in practice, all have ≥3)
- `passage` is ≥100 characters
- `counterexample` references key terms from ≥30% of stated conditions (keyword overlap check)
- AbdCx: `background_cases` is a list of ≥2 items; `abductive_insight` is present and ≥10 characters

### Deduplication
- TF-IDF cosine similarity computed across all passages
- Pairs exceeding 0.85 similarity are flagged as near-duplicates
- The later duplicate is removed

### Validation Results
- DefCx: 3,276 valid, 0 invalid
- AbdCx: 1,198 valid, 0 invalid
- Near-duplicates removed: minimal (≤1 pair in original corpus)

## Quality Characteristics

### What Makes a Good Counterexample
Each counterexample must satisfy several criteria:
1. **Non-triviality:** The gap in the definition is structural, not a trick of verbal ambiguity
2. **Condition coverage:** The counterexample scenario explicitly addresses the stated conditions
3. **Specificity:** The scenario is concrete and detailed, not abstract or schematic
4. **Insight:** The missing condition (if identified) genuinely explains the gap

### Diversity
- **Attack direction:** Automated heuristic classification of all 4,474 entries found that 50.4% demonstrate the definition is too weak (all conditions hold, concept fails), 28.4% too strong (concept applies, condition(s) not met), 15.9% both, and 5.3% ambiguous. See [COUNTEREXAMPLE_DIRECTION.md](COUNTEREXAMPLE_DIRECTION.md) for the full analysis.
- Within each subdomain, different concepts and different definitions are examined
- Counterexample structures vary (thought experiments, real-world scenarios, edge cases, limit cases)

## Limitations
- **Synthetic data:** All examples were generated by an LLM, not extracted from published philosophical literature
- **Style uniformity:** The enforced analytic register means the dataset does not represent the full diversity of philosophical writing
- **No human quality ratings:** The `quality` field is reserved but unpopulated; human evaluation would strengthen confidence in example quality
- **Domain balance:** Domain sizes vary (120-300 DefCx per domain) reflecting judgments about the richness of counterexample opportunities in each area

## Reproducing the Dataset
The generation and validation scripts are included in `scripts/data/sft/`:
- `domains.py` — Domain definitions, subdomains, and target counts
- `generate.py` — Batch generation (API mode or manual import)
- `validate.py` — Structural validation and deduplication
- `format_sft.py` — Convert validated JSONL to training format
- `prepare_release.py` (in `scripts/`) — Split by domain and generate browse files
