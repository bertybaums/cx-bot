# Counterexample Direction Analysis

## Overview

A counterexample to a definition stated as necessary and sufficient conditions can reveal that the definition is defective in two distinct ways:

- **Too weak (insufficient):** All stated conditions are satisfied, yet the concept fails to apply. The definition lets in cases it should exclude. This is the classic Gettier-style move: a scenario satisfies justified-true-belief but is plainly not knowledge, revealing that the conditions are not jointly sufficient.

- **Too strong (over-restrictive):** The concept genuinely applies, but one or more conditions are not met. The definition rules out cases it should include. For example, requiring that tragedy stem from the protagonist's own character flaw excludes tragedies of fate or circumstance.

A counterexample may also reveal **both** defects simultaneously, or the direction may be **ambiguous** from the text alone.

This report classifies all 4,474 entries in the cx-bot corpus by counterexample direction using automated heuristic analysis of the `missing_condition`, `passage`, `counterexample`, and `abductive_insight` fields.

## Results

| Classification | Count | % | Description |
|---|---:|---:|---|
| **Too weak** | 2,253 | 50.4% | Conditions met, concept fails |
| **Too strong** | 1,271 | 28.4% | Concept applies, condition(s) not met |
| **Both** | 713 | 15.9% | Signals in both directions |
| **Ambiguous** | 237 | 5.3% | Unclassifiable by heuristics |

### By entry type

|  | Too weak | Too strong | Both | Ambiguous | Total |
|---|---:|---:|---:|---:|---:|
| **DefCx** | 1,622 (49.5%) | 999 (30.5%) | 549 (16.8%) | 106 (3.2%) | 3,276 |
| **AbdCx** | 631 (52.7%) | 272 (22.7%) | 164 (13.7%) | 131 (10.9%) | 1,198 |

AbdCx entries have a higher ambiguous rate because 148 of the 237 ambiguous entries have null `missing_condition` fields, concentrated in the AbdCx format.

### By domain

| Domain | Weak | Strong | Both | Ambig | Total |
|---|---:|---:|---:|---:|---:|
| Aesthetics | 122 | 113 | 53 | 10 | 298 |
| Epistemology | 248 | 34 | 49 | 4 | 335 |
| Ethics | 195 | 81 | 19 | 10 | 305 |
| Everyday Concepts | 111 | 94 | 48 | 17 | 270 |
| Law | 141 | 93 | 51 | 12 | 297 |
| Logic | 102 | 120 | 57 | 17 | 296 |
| Mathematics | 148 | 66 | 37 | 45 | 296 |
| Metaphysics | 123 | 98 | 40 | 10 | 271 |
| Natural Science | 117 | 97 | 54 | 18 | 286 |
| Phil. of History | 132 | 59 | 37 | 6 | 234 |
| Phil. of Language | 112 | 74 | 70 | 23 | 279 |
| Phil. of Mind | 163 | 60 | 44 | 17 | 284 |
| Phil. of Religion | 128 | 82 | 43 | 13 | 266 |
| Phil. of Science | 161 | 40 | 22 | 11 | 234 |
| Political Phil. | 177 | 40 | 38 | 13 | 268 |
| Social Phil. | 73 | 120 | 51 | 11 | 255 |

## Interpretation

### The dataset is predominantly "too weak" but not overwhelmingly so

About half the corpus (50.4%) follows the classic pattern: all conditions hold, yet the concept fails. This is the most familiar kind of philosophical counterexample and the one most naturally elicited by the generation prompt ("construct a scenario where all conditions hold but the concept fails").

However, a substantial minority (28.4%) demonstrates the opposite: the concept genuinely applies but the definition's conditions exclude it. The "both" category (15.9%) contains entries where the text signals defects in both directions, often in passages that are particularly philosophically rich.

### Domain variation reflects disciplinary character

**Epistemology** is overwhelmingly "too weak" (74%), which is expected: the Gettier tradition that dominates post-1963 epistemology consists precisely in constructing cases where justified-true-belief is satisfied but knowledge is absent.

**Logic** and **social philosophy** lean toward "too strong" (41% and 47% respectively). In logic, this often takes the form of definitions that impose conditions specific to classical systems but fail to accommodate non-classical cases. In social philosophy, definitions frequently encode culturally specific assumptions that exclude legitimate instances from other traditions.

**Philosophy of language** has the highest "both" rate (25%), reflecting the field's characteristic concern with definitions that simultaneously over-generate in some contexts and under-generate in others.

### The "ambiguous" residual

The 237 ambiguous entries fall into two groups:
- **148 entries** (62%) have null or empty `missing_condition` fields, mostly in AbdCx entries, making them unclassifiable by text heuristics alone.
- **89 entries** (38%) have text that doesn't clearly signal direction through the keyword patterns used.

## Methodology

Classification was performed by `scripts/classify_cx_direction.py`, which applies regex-based heuristic patterns to the `missing_condition`, `passage`, `counterexample`, and `abductive_insight` fields.

### "Too weak" signals
Patterns indicating the definition is insufficient / overly permissive:
- Explicit language: "insufficiency", "not sufficient", "too broad/permissive"
- Condition satisfaction: "all conditions are met/satisfied/hold... yet"
- Missing requirements: "omits any requirement", "does not require", "fails to require"
- Permissiveness: "permits cases", "lets in", "admits cases"

### "Too strong" signals
Patterns indicating the definition is over-restrictive:
- Explicit language: "too restrictive/narrow/stringent", "unduly restrict"
- Exclusion of genuine cases: "excludes cases", "fails to accommodate", "cannot accommodate"
- Unnecessary conditions: "the definition requires X, but", "the definition wrongly equates/confuses/assumes"
- Concept applies despite failing conditions: "may also consist in", "may emerge from"
- Empirical refutation: "the history of [field] shows/teaches"

### Classification logic
- If explicit "both" patterns match → **Both**
- If only weak signals match → **Too weak**
- If only strong signals match → **Too strong**
- If both match with a ≥2:1 ratio → the dominant direction; otherwise → **Both**
- If neither matches → **Ambiguous**

### Per-entry results

Detailed per-entry classifications are in [`data/classification_results.json`](data/classification_results.json), with fields: `id`, `type`, `domain`, `subdomain`, `classification`, `weak_score`, `strong_score`.

## Examples

### Too weak

> **Definition:** A person knows that *p* if and only if (i) *p* is true, (ii) they believe that *p*, and (iii) they are justified in believing that *p*.
>
> **Counterexample:** A man glances at a clock on a public building and forms the belief that it is exactly two o'clock. The clock has, in fact, stopped twelve hours previously, yet by sheer coincidence the man happens to look at precisely two o'clock.
>
> All three conditions are satisfied — the belief is true, held, and justified — yet we should hesitate to say he knows the time. The definition **lets in** a case it should exclude.

### Too strong

> **Definition:** A dramatic work is a tragedy if and only if (i) its protagonist suffers a reversal of fortune, (ii) the reversal arises from the protagonist's own actions or character, and (iii) the work elicits pity and fear in the audience.
>
> **Counterexample:** A melodrama depicts a wholly virtuous heroine whose fortune is destroyed by a villain's machinations. The audience feels pity and fear, and there is a clear reversal, but the reversal does not arise from the heroine's own character.
>
> The work is plainly a tragedy, yet condition (ii) is not met. The definition **rules out** a case it should include.
