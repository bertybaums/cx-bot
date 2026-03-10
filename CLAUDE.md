# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A corpus of **4,474 philosophical counterexamples** across **16 domains** for training language models to recognise and generate counterexamples to definitions stated as necessary and sufficient conditions. Includes a QLoRA fine-tuning pipeline and a three-tier evaluation framework.

Generalised from the `gettier` project (sibling directory), which deliberately excluded epistemology. This project **includes epistemology** alongside all 15 other domains.

GitHub: `https://github.com/bertybaums/cx-bot`

## Repository Structure

```
cx-bot/
├── data/
│   ├── defcx/             ← 16 JSONL files, one per domain (3,276 DefCx)
│   ├── abdcx/             ← 16 JSONL files, one per domain (1,198 AbdCx)
│   ├── training/          ← Merged train/val splits (EOT-separated text)
│   └── README.md          ← Schema documentation
├── examples/              ← Browsable passages by domain (Markdown)
├── scripts/data/sft/      ← Generation, validation, formatting scripts
├── train/
│   ├── sft_qlora.py       ← QLoRA SFT training script (Unsloth + TRL)
│   └── submit.slurm       ← SLURM job for HPC training
├── eval/
│   ├── generate.py        ← GPU inference with LoRA adapter
│   ├── score.py           ← Tier 1 (structural) + Tier 2 (register) scoring
│   ├── judge.py           ← Tier 3 LLM-as-judge for logical quality
│   └── submit_generate.slurm
├── README.md
├── METHODOLOGY.md
└── LICENSE                ← CC-BY-4.0
```

## Data Formats

**DefCx** (Definition + Counterexample):
- Fields: `id`, `domain`, `subdomain`, `definition`, `conditions`, `counterexample`, `missing_condition`, `passage`
- Definition stated as necessary and sufficient conditions; scenario constructed where all conditions hold but concept fails

**AbdCx** (Abductive Counterexample):
- Fields: all DefCx fields plus `background_cases`, `abductive_insight`
- Background cases motivate a definition; counterexample exploits what the cases shared but the definition dropped

## Dataset Stats

| | DefCx | AbdCx | Total |
|---|------:|------:|------:|
| **Examples** | 3,276 | 1,198 | 4,474 |
| **Domains** | 16 | 16 | 16 |
| **Subdomains** | 130+ | 130+ | 130+ |

## Training Pipeline

### QLoRA SFT (completed)

Trained on `fortyfive.hpc.uidaho.edu` (SLURM cluster).

- **Base model:** Qwen2.5-3B-Instruct (4-bit quantized via Unsloth)
- **LoRA:** r=16, alpha=16, targets all attention + MLP projections (0.96% trainable)
- **Data:** 4,251 train / 223 val (95/5 split), chat format (system/user/assistant)
- **Hyperparams:** batch=4, grad_accum=4 (eff=16), lr=2e-4, cosine schedule, 3 epochs, fp16
- **Result:** 798 steps in 1h32m, final train loss 0.60, eval loss 0.68
- **Adapter:** `outputs/cx-bot-qwen3b-qlora/lora/` on HPC (115MB)
- **Venv:** Reuses `~/ARC/venv/` (Unsloth 2025.8.6, TRL 0.21.0, PyTorch 2.8.0)

Chat format for training:
```
system  → philosopher persona + output schema (SYSTEM_PROMPT in sft_qlora.py)
user    → "Produce a {DefCx|AbdCx} example for the domain of {domain}, subdomain: {subdomain}."
assistant → structured JSON (definition, conditions, counterexample, passage, etc.)
```

### HPC Notes

- **Exclude n113** from GPU jobs (GTX 1080 Ti, sm_61 — incompatible with PyTorch build)
- CUDA/python module loads are non-fatal (`|| true`) since some nodes lack modulefiles
- ARC venv python symlink fixed to `/opt/modules/devel/python/3.11.11/bin/python3.11`

## Evaluation Framework

Three tiers, tested on 235 generated completions:

### Tier 1 — Structural (automated) → 98.3% pass
- JSON validity, required fields, conditions ≥ 3, passage length ≥ 150/200 words
- Condition overlap ≥ 30% (counterexample references stated conditions)
- Background cases ≥ 2 (AbdCx only)

### Tier 2 — Register & Style (automated heuristics) → 51.9% pass
- Hedging phrases ≥ 2 (this is the main bottleneck; ≥1 would give ~99%)
- British spelling (no American variants)
- No forbidden patterns (bullets, markdown, "counterexample" in passages)

### Tier 3 — Logical Quality (LLM-as-judge) → mean 4.27/9
Assessed on 15-sample cross-domain evaluation:
- **Condition satisfaction:** Do stated conditions genuinely hold? (mean 1.27/3)
- **Definition defeat:** Does the scenario reveal genuine insufficiency? (mean 1.40/3)
- **Insight quality:** Is the identified gap substantive? (mean 1.60/3)
- ~30% strong (7+/9), ~33% middling (4-6/9), ~37% weak (0-3/9)

### Novelty
- Zero near-duplicates (max TF-IDF similarity to training: 0.70, threshold: 0.85)
- Model generates genuinely novel counterexamples, not memorised training data

## Key Finding

SFT achieved excellent structural quality but inconsistent logical coherence. The main failure mode is claiming conditions are satisfied when the described scenario doesn't actually satisfy them. This is the kind of reasoning deficit that RL with a logical-quality reward signal could potentially address.

## Scripts Reference

### Data scripts (`scripts/data/sft/`)
- `domains.py` — 16 domain definitions, register guidelines
- `generate.py` — Batch generation via Anthropic API or manual import
- `validate.py` — Structural validation, condition overlap, TF-IDF dedup
- `format_sft.py` — Convert validated JSONL to EOT-separated text

### Training (`train/`)
- `sft_qlora.py` — Full QLoRA SFT script (Unsloth + TRL)
- `submit.slurm` — SLURM submission for gpu-8 partition

### Evaluation (`eval/`)
- `generate.py` — Inference with LoRA adapter, auto-samples prompts from data/
- `score.py` — Tier 1 + Tier 2 + TF-IDF novelty scoring
- `judge.py` — Tier 3 LLM-as-judge (export or API mode)
- `submit_generate.slurm` — SLURM submission for generation

## Register

All passages written in the style of early-to-mid twentieth-century analytic philosophy (Russell, Moore, Ayer, Broad, Ryle): continuous prose, British spelling, hedging language, no modern jargon or formatting. See `REGISTER_GUIDELINES` in `domains.py`.
