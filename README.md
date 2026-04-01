# CX-Bot: A Corpus of Philosophical Counterexamples

A dataset of **4,474 philosophical counterexamples** across **16 domains**, designed for training language models to recognise and generate counterexamples to definitions stated as necessary and sufficient conditions.

Each example presents a proposed definition, constructs a concrete scenario revealing its structural insufficiency, and (where applicable) identifies the missing condition that would repair the analysis. About half the counterexamples show the definition is **too weak** (conditions met, concept fails); about a quarter show it is **too strong** (concept applies, condition not met); the remainder show both or are ambiguous. See [COUNTEREXAMPLE_DIRECTION.md](COUNTEREXAMPLE_DIRECTION.md) for the full analysis. All passages are written in the style of early-to-mid twentieth-century analytic philosophy.

## Quick Start

**Browse examples:** See the [examples/](examples/) directory for readable passages organised by domain.

**Use the data:** JSONL files are in [`data/defcx/`](data/defcx/) and [`data/abdcx/`](data/abdcx/), one file per domain.

**Train a model:** Pre-formatted train/val splits are in [`data/training/`](data/training/).

## Dataset at a Glance

| | DefCx | AbdCx | Total |
|---|------:|------:|------:|
| **Examples** | 3,276 | 1,198 | 4,474 |
| **Domains** | 16 | 16 | 16 |
| **Subdomains** | 130+ | 130+ | 130+ |

### Two Formats

**DefCx** (Definition + Counterexample): A definition is stated as necessary and sufficient conditions; a scenario is constructed revealing the definition is too weak (conditions hold, concept fails), too strong (concept applies, conditions not met), or both.

**AbdCx** (Abductive Counterexample): Background cases motivate a definition; the counterexample exploits a feature the cases shared but the definition missed. Includes an explicit abductive insight.

### Domain Coverage

| Domain | DefCx | AbdCx | | Domain | DefCx | AbdCx |
|--------|------:|------:|-|--------|------:|------:|
| Aesthetics | 214 | 84 | | Logic | 213 | 83 |
| Epistemology | 250 | 85 | | Mathematics | 214 | 82 |
| Ethics | 220 | 85 | | Metaphysics | 194 | 77 |
| Everyday Concepts | 193 | 77 | | Natural Science | 207 | 79 |
| Law | 223 | 74 | | Phil. of History | 170 | 64 |
| Phil. of Language | 208 | 71 | | Phil. of Religion | 200 | 66 |
| Phil. of Mind | 207 | 77 | | Phil. of Science | 168 | 66 |
| Political Phil. | 202 | 66 | | Social Phil. | 193 | 62 |

## Example

From the epistemology/knowledge subdomain (DefCx):

> **Definition:** A person knows that *p* if and only if (i) *p* is true, (ii) he believes that *p*, and (iii) he is justified in believing that *p*.

> The proposed analysis holds that a person knows that *p* if and only if *p* is true, he believes it, and he is justified in so believing. Upon examination, however, one may construct a case which reveals the insufficiency of this analysis. Consider a man who looks at a clock in the town square and forms the belief that it is exactly two o'clock. The clock reads two o'clock, and it is indeed two o'clock — the proposition is true. He has every reason to trust the clock, which has been reliable for years, so his belief is justified. Yet the clock stopped exactly twelve hours ago. His belief is true, justified, and believed, but we should hesitate to say he *knows* that it is two o'clock, for the correctness of his belief is entirely a matter of luck.

## Repository Structure

```
cx-bot/
├── README.md                      ← You are here
├── METHODOLOGY.md                 ← How examples were created and validated
├── COUNTEREXAMPLE_DIRECTION.md    ← Too-weak vs too-strong analysis
├── LICENSE                        ← CC-BY-4.0
├── examples/              ← Browsable passages by domain (Markdown)
├── data/
│   ├── defcx/             ← DefCx JSONL files (one per domain)
│   ├── abdcx/             ← AbdCx JSONL files (one per domain)
│   ├── training/          ← Merged train/val splits (EOT-separated text)
│   └── README.md          ← Schema documentation
└── scripts/
    ├── data/sft/          ← Generation, validation, formatting scripts
    └── prepare_release.py ← Split by domain and generate browse files
```

## Schema

### DefCx Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `domain` | string | Philosophical domain |
| `subdomain` | string | Specific subdomain |
| `definition` | string | Proposed definition |
| `conditions` | list | Individual conditions (≥3) |
| `counterexample` | string | Scenario revealing insufficiency |
| `missing_condition` | string/null | Gap the definition failed to capture |
| `passage` | string | Full prose passage (≥150 words) |

### Additional AbdCx Fields

| Field | Type | Description |
|-------|------|-------------|
| `background_cases` | list | 2-4 motivating cases |
| `abductive_insight` | string | What was lost in the abstraction |

See [`data/README.md`](data/README.md) for full schema documentation.

## Methodology

All examples were generated using Claude (Anthropic) and validated through a structural pipeline checking field completeness, condition coverage, passage length, and near-duplicate detection via TF-IDF cosine similarity. See [METHODOLOGY.md](METHODOLOGY.md) for full details and [COUNTEREXAMPLE_DIRECTION.md](COUNTEREXAMPLE_DIRECTION.md) for the too-weak vs too-strong breakdown.

## License

This dataset is released under the [Creative Commons Attribution 4.0 International License](LICENSE) (CC-BY-4.0).

## Citation

```bibtex
@misc{cxbot2025,
  title={CX-Bot: A Corpus of Philosophical Counterexamples},
  author={Baum, B.},
  year={2025},
  url={https://github.com/bertybaums/cx-bot}
}
```
