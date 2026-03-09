"""
Domain definitions and register guidelines for SFT data.

Generalised from the gettier project — all domains including epistemology.
Pure data module — no external dependencies.
"""

import re


# ── Domain definitions ──
# Each domain contributes examples to both DefCx and AbdCx datasets.
# Unlike the gettier project, epistemology is included here.

DOMAINS = [
    {
        "name": "ethics",
        "subdomains": [
            "virtue_theory", "justice", "moral_obligation", "rights",
            "desert", "consent", "punishment", "promise_keeping",
            "moral_responsibility", "moral_luck",
        ],
        "defcx_target": 300,
        "abdcx_target": 100,
    },
    {
        "name": "aesthetics",
        "subdomains": [
            "beauty", "art", "sublimity", "taste",
            "aesthetic_experience", "representation", "expression",
        ],
        "defcx_target": 200,
        "abdcx_target": 80,
    },
    {
        "name": "political_philosophy",
        "subdomains": [
            "democracy", "freedom", "equality", "authority",
            "legitimacy", "sovereignty", "civil_disobedience", "rights",
        ],
        "defcx_target": 200,
        "abdcx_target": 80,
    },
    {
        "name": "philosophy_of_mind",
        "subdomains": [
            "consciousness", "intention", "personal_identity", "free_will",
            "action", "emotion", "perception", "memory",
        ],
        "defcx_target": 250,
        "abdcx_target": 100,
    },
    {
        "name": "philosophy_of_language",
        "subdomains": [
            "meaning", "reference", "naming", "translation",
            "metaphor", "speech_acts", "vagueness",
        ],
        "defcx_target": 200,
        "abdcx_target": 70,
    },
    {
        "name": "mathematics",
        "subdomains": [
            "primality", "continuity", "convergence", "connectedness",
            "computability", "cardinality", "completeness", "decidability",
        ],
        "defcx_target": 300,
        "abdcx_target": 100,
    },
    {
        "name": "logic",
        "subdomains": [
            "validity", "soundness", "logical_consequence", "paradoxes",
            "entailment", "consistency", "definability",
        ],
        "defcx_target": 200,
        "abdcx_target": 70,
    },
    {
        "name": "law",
        "subdomains": [
            "contract", "property", "negligence", "person",
            "consent", "self_defence", "causation", "liability",
        ],
        "defcx_target": 250,
        "abdcx_target": 100,
    },
    {
        "name": "natural_science",
        "subdomains": [
            "species", "life", "planet", "element",
            "disease", "ecosystem", "gene", "force",
        ],
        "defcx_target": 200,
        "abdcx_target": 80,
    },
    {
        "name": "everyday_concepts",
        "subdomains": [
            "game", "chair", "art", "language",
            "lie", "promise", "vehicle", "tool",
        ],
        "defcx_target": 150,
        "abdcx_target": 50,
    },
    {
        "name": "metaphysics",
        "subdomains": [
            "substance", "causation_metaphysical", "time", "space",
            "identity_metaphysical", "universals", "possibility",
            "necessity", "change", "persistence", "mereology",
            "modality",
        ],
        "defcx_target": 180,
        "abdcx_target": 65,
    },
    {
        "name": "philosophy_of_science",
        "subdomains": [
            "explanation", "scientific_law", "theory", "observation",
            "reduction", "experiment", "measurement", "prediction",
            "classification", "model", "falsifiability", "paradigm",
        ],
        "defcx_target": 150,
        "abdcx_target": 55,
    },
    {
        "name": "philosophy_of_religion",
        "subdomains": [
            "existence_of_god", "problem_of_evil", "miracle", "faith",
            "prayer", "sacred", "revelation", "divine_command",
            "immortality", "religious_experience",
        ],
        "defcx_target": 130,
        "abdcx_target": 50,
    },
    {
        "name": "social_philosophy",
        "subdomains": [
            "community", "tradition", "custom", "institution",
            "culture", "norm", "cooperation", "trust",
            "alienation", "social_contract",
        ],
        "defcx_target": 130,
        "abdcx_target": 50,
    },
    {
        "name": "philosophy_of_history",
        "subdomains": [
            "progress", "historical_explanation", "periodisation",
            "civilisation", "decline", "tradition_historical",
            "narrative", "anachronism", "legacy", "revolution_historical",
        ],
        "defcx_target": 120,
        "abdcx_target": 45,
    },
    # ── NEW: epistemology ──
    # The gettier project excluded this domain to keep evaluation clean.
    # Here we include it — the post-Gettier literature provides a rich
    # source of counterexamples to definitions of knowledge, justification,
    # belief, and related concepts.
    {
        "name": "epistemology",
        "subdomains": [
            "knowledge", "justification", "belief", "perception",
            "testimony", "memory_epistemic", "a_priori",
            "skepticism", "truth", "epistemic_virtue",
        ],
        "defcx_target": 250,
        "abdcx_target": 85,
    },
]


# ── Register guidelines ──
# Embedded in generation prompts to enforce style consistency.

REGISTER_GUIDELINES = """\
Write in the style of early-to-mid twentieth-century analytic philosophy \
(Russell, Moore, Ayer, Broad, Ryle). Observe the following conventions:

1. Use continuous prose paragraphs. Never use bullet points, numbered lists, \
or section headers.
2. Employ hedging language where appropriate: "one might observe," \
"it appears," "we should hesitate to say," "it is by no means certain."
3. Use British spelling: "analyse," "defence," "behaviour," "recognise," \
"colour," "honour," "favour."
4. Prefer the impersonal or first-person plural: "one may construct \
a case," "we are led to conclude," "it will be observed."
5. Avoid modern jargon, abbreviations, emoji, and formatting conventions \
such as Markdown or LaTeX.
6. Each passage should read as an excerpt from a philosophy journal article \
of the period 1920-1960.
7. Definitions should be stated as necessary and jointly sufficient \
conditions, using the form "X is Y if and only if (i) ..., (ii) ..., \
and (iii) ...".
8. Counterexamples should be introduced with phrases like "Consider a case \
in which," "Suppose that," or "Let us imagine."
9. Do not use the word "counterexample" — instead speak of "a case which \
reveals the insufficiency of this analysis" or "an instance that tells \
against the proposed definition."
"""


def get_domain_by_name(name):
    """Look up a domain dict by name. Returns None if not found."""
    for d in DOMAINS:
        if d["name"] == name:
            return d
    return None


def all_domain_names():
    """Return sorted list of all domain names."""
    return sorted(d["name"] for d in DOMAINS)
