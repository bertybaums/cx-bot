#!/usr/bin/env python3
"""
CX-Bot SFT with QLoRA (Unsloth + TRL) on Qwen2.5-3B-Instruct.

Trains a LoRA adapter to generate philosophical counterexamples in
DefCx and AbdCx format.

Each JSONL record is formatted as a chat conversation:
  system  → philosopher persona + output schema
  user    → domain, subdomain, task type (defcx/abdcx)
  assistant → structured JSON with definition, conditions, counterexample, passage

Save outputs:
  <output_dir>/lora/  (LoRA adapter + tokenizer)
  Optionally: <output_dir>/merged-16bit/
"""

from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template

import os
import json
import argparse
import random
from pathlib import Path
from typing import List, Dict, Any

import torch
from datasets import Dataset, DatasetDict
from trl import SFTTrainer, SFTConfig
from transformers import set_seed


# ── System prompt ──

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


# ── Data loading ──

# Fields to include in the assistant response (strip metadata)
DEFCX_FIELDS = [
    "definition", "conditions", "counterexample",
    "missing_condition", "passage",
]

ABDCX_FIELDS = [
    "background_cases", "definition", "conditions",
    "counterexample", "abductive_insight", "passage",
]


def record_to_conversation(record: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    """Convert a JSONL record to a chat conversation."""
    domain = record.get("domain", "philosophy")
    subdomain = record.get("subdomain", "general").replace("_", " ")

    # Detect format
    is_abdcx = "background_cases" in record or "abductive_insight" in record
    task_type = "AbdCx" if is_abdcx else "DefCx"
    fields = ABDCX_FIELDS if is_abdcx else DEFCX_FIELDS

    # Build user prompt
    user_content = (
        f"Produce a {task_type} example for the domain of "
        f"{domain.replace('_', ' ')}, subdomain: {subdomain}."
    )

    # Build assistant response (structured JSON, no metadata)
    response = {k: record[k] for k in fields if k in record}
    assistant_content = json.dumps(response, ensure_ascii=False, indent=None)

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
    }


def load_jsonl_dir(data_dir: str) -> List[Dict[str, Any]]:
    """Load all JSONL files from a directory."""
    records = []
    for path in sorted(Path(data_dir).glob("*.jsonl")):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return records


def build_datasets(
    defcx_dir: str,
    abdcx_dir: str,
    seed: int,
    val_ratio: float,
) -> DatasetDict:
    """Load data, format as conversations, split into train/val."""
    # Load records
    defcx_records = load_jsonl_dir(defcx_dir)
    abdcx_records = load_jsonl_dir(abdcx_dir)
    print(f"Loaded {len(defcx_records)} DefCx + {len(abdcx_records)} AbdCx "
          f"= {len(defcx_records) + len(abdcx_records)} total")

    # Convert to conversations
    conversations = []
    for rec in defcx_records:
        conversations.append(record_to_conversation(rec))
    for rec in abdcx_records:
        conversations.append(record_to_conversation(rec))

    # Shuffle and split
    random.seed(seed)
    random.shuffle(conversations)

    ds_all = Dataset.from_list(conversations)
    n = len(ds_all)
    n_val = max(1, int(val_ratio * n))

    ds = DatasetDict({
        "train": ds_all.select(range(n - n_val)),
        "validation": ds_all.select(range(n - n_val, n)),
    })

    return ds


# ── Formatting function for TRL ──

tokenizer = None


def formatting_func(examples):
    """Format chat messages for SFTTrainer."""
    global tokenizer

    conversations = examples["messages"]

    # Handle single (unbatched) example
    if conversations and isinstance(conversations[0], dict):
        conversations = [conversations]

    outputs = []
    for conversation in conversations:
        formatted_text = tokenizer.apply_chat_template(
            conversation,
            tokenize=False,
            add_generation_prompt=False,
        )
        outputs.append(formatted_text)

    return outputs


# ── Main ──

def main():
    global tokenizer

    parser = argparse.ArgumentParser(
        description="CX-Bot SFT (QLoRA) on Qwen2.5-3B-Instruct")

    # Data
    parser.add_argument("--defcx_dir", default="data/defcx",
                        help="Directory with DefCx JSONL files")
    parser.add_argument("--abdcx_dir", default="data/abdcx",
                        help="Directory with AbdCx JSONL files")
    parser.add_argument("--output_dir", default="outputs/cx-bot-qwen3b-qlora",
                        help="Where to save checkpoints/adapters")

    # Model
    parser.add_argument("--model_name", default="unsloth/Qwen2.5-3B-Instruct",
                        help="Base model (Unsloth-optimized)")
    parser.add_argument("--max_seq_len", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--val_ratio", type=float, default=0.05)

    # LoRA / QLoRA
    parser.add_argument("--r", type=int, default=16,
                        help="LoRA rank")
    parser.add_argument("--lora_alpha", type=int, default=16,
                        help="LoRA alpha (scaling = alpha/r)")
    parser.add_argument("--lora_dropout", type=float, default=0.0)
    parser.add_argument(
        "--target_modules", nargs="+",
        default=["q_proj", "k_proj", "v_proj", "o_proj",
                 "gate_proj", "up_proj", "down_proj"],
        help="LoRA target modules")

    # Training
    parser.add_argument("--batch_size", type=int, default=4,
                        help="Per-device train batch size")
    parser.add_argument("--grad_accum", type=int, default=4,
                        help="Gradient accumulation steps (effective batch = batch_size * grad_accum)")
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--warmup_ratio", type=float, default=0.03)
    parser.add_argument("--logging_steps", type=int, default=10)
    parser.add_argument("--save_steps", type=int, default=200)
    parser.add_argument("--eval_steps", type=int, default=200)
    parser.add_argument("--bf16", action="store_true",
                        help="Use BF16 (A6000 supports this)")
    parser.add_argument("--packing", action="store_true",
                        help="Enable sequence packing")
    parser.add_argument("--save_merged_16bit", action="store_true",
                        help="Also save merged 16-bit model")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    set_seed(args.seed)

    # 1) Build datasets
    ds = build_datasets(
        defcx_dir=args.defcx_dir,
        abdcx_dir=args.abdcx_dir,
        seed=args.seed,
        val_ratio=args.val_ratio,
    )

    # 2) Load model + tokenizer
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model_name,
        max_seq_length=args.max_seq_len,
        dtype=None,
        load_in_4bit=True,
        device_map="auto",
    )

    tokenizer = get_chat_template(tokenizer, chat_template="qwen-2.5")

    # 3) Apply LoRA
    model = FastLanguageModel.get_peft_model(
        model,
        r=args.r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=args.target_modules,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    # 4) Training config
    training_args = SFTConfig(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type="cosine",
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        eval_strategy="steps",
        eval_steps=args.eval_steps,
        save_total_limit=2,
        bf16=args.bf16,
        fp16=not args.bf16,
        packing=args.packing,
        eos_token="<|im_end|>",
        pad_token=tokenizer.eos_token,
        optim="paged_adamw_8bit",
        report_to=None,
        max_length=args.max_seq_len,
    )

    # 5) Train
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        args=training_args,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"],
        formatting_func=formatting_func,
    )

    print(f"\n{'='*60}")
    print(f"CX-Bot QLoRA SFT")
    print(f"  Model:     {args.model_name}")
    print(f"  LoRA rank: {args.r}, alpha: {args.lora_alpha}")
    print(f"  Train:     {len(ds['train'])} examples")
    print(f"  Val:       {len(ds['validation'])} examples")
    print(f"  Epochs:    {args.epochs}")
    print(f"  Eff batch: {args.batch_size * args.grad_accum}")
    print(f"  LR:        {args.lr}")
    print(f"  Output:    {args.output_dir}")
    print(f"{'='*60}\n")

    trainer.train()

    # 6) Save LoRA adapter
    lora_dir = os.path.join(args.output_dir, "lora")
    os.makedirs(lora_dir, exist_ok=True)
    model.save_pretrained(lora_dir)
    tokenizer.save_pretrained(lora_dir)
    print(f"\n[OK] Saved LoRA adapter to: {lora_dir}")

    # 7) Optional: save merged model
    if args.save_merged_16bit:
        merged_dir = os.path.join(args.output_dir, "merged-16bit")
        os.makedirs(merged_dir, exist_ok=True)
        model.save_pretrained_merged(
            merged_dir, tokenizer, save_method="merged_16bit")
        print(f"[OK] Saved merged 16-bit model to: {merged_dir}")

    # 8) Save training config for reproducibility
    config_path = os.path.join(args.output_dir, "training_config.json")
    with open(config_path, "w") as f:
        json.dump(vars(args), f, indent=2)
    print(f"[OK] Saved config to: {config_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
