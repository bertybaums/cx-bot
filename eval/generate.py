#!/usr/bin/env python3
"""
CX-Bot Evaluation: Generate completions from a fine-tuned model.

Loads base model + LoRA adapter via Unsloth and generates structured
counterexamples for evaluation. Prompts are sampled from the data
directory (one per domain/subdomain/task_type combination) or read
from a custom JSONL file.

Usage:
    # Auto-sample 3 prompts per subdomain from data/
    python eval/generate.py \
        --lora_dir outputs/cx-bot-qwen3b-qlora/lora \
        --output eval/results/completions.jsonl \
        --n_per_subdomain 3

    # Use custom prompts
    python eval/generate.py \
        --lora_dir outputs/cx-bot-qwen3b-qlora/lora \
        --prompts eval/my_prompts.jsonl \
        --output eval/results/completions.jsonl

    # Base model only (no adapter, for comparison)
    python eval/generate.py \
        --base_only \
        --output eval/results/completions_base.jsonl
"""

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

import argparse
import json
import os
import random
import time
from pathlib import Path

import torch


# ── System prompt (must match training) ──

SYSTEM_PROMPT = """\
You are a philosopher trained in the analytic tradition of the early-to-mid \
twentieth century (Russell, Moore, Ayer, Broad, Ryle). You examine definitions \
of concepts by constructing cases that reveal their insufficiency.

When asked to produce a DefCx example, respond with a JSON object containing:
- "definition": the proposed definition as necessary and sufficient conditions
- "conditions": a list of individual conditions (at least 3)
- "counterexample": a scenario where conditions hold but the concept fails (2-3 sentences)
- "missing_condition": what the definition failed to capture (1 sentence, or null)
- "passage": a full prose passage (at least 150 words) in analytic philosophy style

When asked to produce an AbdCx example, respond with a JSON object containing:
- "background_cases": a list of 2-4 motivating cases
- "definition": the definition extracted from those cases
- "conditions": a list of individual conditions (at least 3)
- "counterexample": a scenario exploiting what the cases shared but the definition missed
- "abductive_insight": what was lost in the abstraction (1-2 sentences)
- "passage": a full prose passage (at least 200 words) in analytic philosophy style

Use British spelling. Write in continuous prose with hedging language. \
Do not use the word "counterexample" in passages."""


# ── Prompt construction ──

def get_domain_subdomains(data_dir):
    """Read domain/subdomain pairs from JSONL data files."""
    combos = {}
    for kind in ["defcx", "abdcx"]:
        d = Path(data_dir) / kind
        if not d.exists():
            continue
        for f in sorted(d.glob("*.jsonl")):
            domain = f.stem
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    sub = rec.get("subdomain", "general")
                    combos.setdefault(domain, set()).add(sub)
    return {k: sorted(v) for k, v in sorted(combos.items())}


def build_prompts(data_dir, n_per_subdomain, seed=42):
    """Build evaluation prompts: n per subdomain, alternating DefCx/AbdCx."""
    random.seed(seed)
    domain_subs = get_domain_subdomains(data_dir)

    prompts = []
    for domain, subs in domain_subs.items():
        for sub in subs:
            for i in range(n_per_subdomain):
                # 2:1 ratio DefCx:AbdCx (matching corpus proportions)
                task = "AbdCx" if i % 3 == 2 else "DefCx"
                prompts.append({
                    "domain": domain,
                    "subdomain": sub,
                    "task_type": task,
                })

    random.shuffle(prompts)
    return prompts


def make_user_prompt(domain, subdomain, task_type):
    """Build the user message for a generation prompt."""
    return (
        f"Produce a {task_type} example for the domain of "
        f"{domain.replace('_', ' ')}, subdomain: {subdomain.replace('_', ' ')}."
    )


# ── Generation ──

def generate_one(model, tokenizer, prompt, max_new_tokens, temperature, top_p):
    """Generate a single completion and return the raw text."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": make_user_prompt(
            prompt["domain"], prompt["subdomain"], prompt["task_type"])},
    ]

    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature if temperature > 0 else 1.0,
            top_p=top_p,
            do_sample=temperature > 0,
        )

    # Decode only the generated portion
    gen_ids = output_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(gen_ids, skip_special_tokens=True)


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description="Generate CX-Bot evaluation completions")

    # Model
    parser.add_argument("--model_name", default="unsloth/Qwen2.5-3B-Instruct")
    parser.add_argument("--lora_dir", default=None,
                        help="Path to saved LoRA adapter directory")
    parser.add_argument("--base_only", action="store_true",
                        help="Run base model without LoRA (for comparison)")
    parser.add_argument("--max_seq_len", type=int, default=2048)

    # Prompts
    parser.add_argument("--prompts", default=None,
                        help="Custom prompts JSONL (each line: domain, subdomain, task_type)")
    parser.add_argument("--data_dir", default="data",
                        help="Data directory for auto-generating prompts")
    parser.add_argument("--n_per_subdomain", type=int, default=3,
                        help="Number of prompts per subdomain (auto mode)")

    # Generation
    parser.add_argument("--output", default="eval/results/completions.jsonl")
    parser.add_argument("--max_new_tokens", type=int, default=1536)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if not args.base_only and args.lora_dir is None:
        parser.error("--lora_dir is required unless --base_only is set")

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    # ── Load model ──
    print("Loading model...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model_name,
        max_seq_length=args.max_seq_len,
        dtype=None,
        load_in_4bit=True,
    )
    tokenizer = get_chat_template(tokenizer, chat_template="qwen-2.5")

    if not args.base_only:
        from peft import PeftModel
        print(f"Loading LoRA adapter from {args.lora_dir}...")
        model = PeftModel.from_pretrained(model, args.lora_dir)

    FastLanguageModel.for_inference(model)
    print("Model ready.\n")

    # ── Build or load prompts ──
    if args.prompts:
        with open(args.prompts) as f:
            prompts = [json.loads(line) for line in f if line.strip()]
        print(f"Loaded {len(prompts)} prompts from {args.prompts}")
    else:
        prompts = build_prompts(args.data_dir, args.n_per_subdomain, args.seed)
        print(f"Generated {len(prompts)} prompts "
              f"({args.n_per_subdomain}/subdomain)")

    # ── Generate ──
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    t0 = time.time()

    with open(args.output, "w") as out:
        for i, prompt in enumerate(prompts):
            raw = generate_one(
                model, tokenizer, prompt,
                args.max_new_tokens, args.temperature, args.top_p,
            )

            record = {
                **prompt,
                "raw_output": raw,
                "lora": not args.base_only,
                "temperature": args.temperature,
                "top_p": args.top_p,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()

            if (i + 1) % 10 == 0 or (i + 1) == len(prompts):
                elapsed = time.time() - t0
                rate = (i + 1) / elapsed
                eta = (len(prompts) - i - 1) / rate if rate > 0 else 0
                print(f"  [{i+1}/{len(prompts)}]  "
                      f"{rate:.1f} it/s  ETA {eta/60:.0f}m")

    elapsed = time.time() - t0
    print(f"\nDone. {len(prompts)} completions in {elapsed/60:.1f}m")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
