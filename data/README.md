# Data Directory

## Structure

```
data/
├── defcx/          # Definition + Counterexample (one JSONL per domain)
├── abdcx/          # Abductive Counterexample (one JSONL per domain)
└── training/       # Merged, shuffled, split for model training
```

## DefCx Schema

Each line in a DefCx JSONL file is a JSON object with:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (`defcx_{domain}_{subdomain}_{NNNN}`) |
| `domain` | string | Philosophical domain |
| `subdomain` | string | Specific subdomain |
| `definition` | string | Proposed definition as necessary & sufficient conditions |
| `conditions` | list[string] | Individual conditions (≥3) |
| `counterexample` | string | Scenario where conditions hold but concept fails (2-3 sentences) |
| `missing_condition` | string or null | What the definition failed to capture |
| `passage` | string | Full prose passage (≥150 words) |
| `source` | string | `"manual"` or `"synthetic"` |
| `quality` | null | Reserved for human quality ratings |

## AbdCx Schema

AbdCx extends the DefCx schema with two additional fields:

| Field | Type | Description |
|-------|------|-------------|
| `background_cases` | list[string] | 2-4 motivating cases that ground the definition |
| `abductive_insight` | string | What the background cases shared that the definition missed |

AbdCx passages are longer (≥200 words) and structured in two phases: background cases → definition → counterexample → insight.

## Training Format

Files in `training/` contain EOT-separated passages:

```
<|endoftext|>
[passage text]
<|endoftext|>
[passage text]
...
```

Generated with a 95/5 train/val split, shuffled with seed 42.
