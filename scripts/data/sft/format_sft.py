#!/usr/bin/env python3
"""
Convert validated JSONL to plain text for SFT training.

Output format: EOT-separated passages.

    <|endoftext|>
    [passage text from example 1]
    <|endoftext|>
    [passage text from example 2]
    ...

Options:
    --shuffle          Randomize order (with seed)
    --split 0.95       Train/val split ratio
    --tokenizer PATH   Report token counts using a project tokenizer

Usage:
    python scripts/data/sft/format_sft.py \
        --input data/sft/defcx_validated.jsonl data/sft/abdcx_validated.jsonl \
        --output-prefix data/sft/combined \
        --shuffle --split 0.95
"""

import argparse
import json
import random
import sys
from pathlib import Path


EOT_TOKEN = "<|endoftext|>"


def load_passages(input_paths):
    """Load passage texts from one or more JSONL files."""
    passages = []
    for path in input_paths:
        path = Path(path)
        if not path.exists():
            print(f"Warning: {path} not found, skipping.")
            continue
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                passage = rec.get("passage", "").strip()
                if passage:
                    passages.append(passage)
    return passages


def format_passages(passages):
    """Format passages as EOT-separated text."""
    parts = []
    for passage in passages:
        parts.append(EOT_TOKEN)
        parts.append(passage)
    return "\n".join(parts) + "\n"


def write_split(passages, output_prefix, split_ratio, seed):
    """Write train/val split files. Returns (train_path, val_path, n_train, n_val)."""
    output_prefix = Path(output_prefix)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    n = len(passages)
    n_train = int(n * split_ratio)
    n_val = n - n_train

    train_passages = passages[:n_train]
    val_passages = passages[n_train:]

    train_path = output_prefix.parent / f"{output_prefix.name}_train.txt"
    val_path = output_prefix.parent / f"{output_prefix.name}_val.txt"

    with open(train_path, "w") as f:
        f.write(format_passages(train_passages))

    with open(val_path, "w") as f:
        f.write(format_passages(val_passages))

    return train_path, val_path, n_train, n_val


def write_single(passages, output_prefix):
    """Write all passages to a single file."""
    output_prefix = Path(output_prefix)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    out_path = output_prefix.parent / f"{output_prefix.name}.txt"
    with open(out_path, "w") as f:
        f.write(format_passages(passages))

    return out_path


def count_tokens(text, tokenizer_path):
    """Count tokens using a BPE tokenizer."""
    try:
        from tokenizers import Tokenizer
    except ImportError:
        print("Warning: 'tokenizers' package not installed. "
              "Skipping token count.")
        return None

    tokenizer_path = Path(tokenizer_path)
    if not tokenizer_path.exists():
        print(f"Warning: tokenizer not found at {tokenizer_path}. "
              f"Skipping token count.")
        return None

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    encoding = tokenizer.encode(text)
    return len(encoding.ids)


def main():
    parser = argparse.ArgumentParser(
        description="Format validated JSONL as EOT-separated text for SFT")
    parser.add_argument(
        "--input", nargs="+", required=True,
        help="Input validated JSONL file(s)")
    parser.add_argument(
        "--output-prefix", required=True,
        help="Output file prefix (e.g., data/sft/combined)")
    parser.add_argument(
        "--shuffle", action="store_true",
        help="Shuffle passages before writing")
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for shuffling (default: 42)")
    parser.add_argument(
        "--split", type=float, default=None,
        help="Train/val split ratio (e.g., 0.95 for 95%% train)")
    parser.add_argument(
        "--tokenizer", default=None,
        help="Path to tokenizer.json for token counting")

    args = parser.parse_args()

    # Load
    passages = load_passages(args.input)
    if not passages:
        print("No passages found. Exiting.")
        sys.exit(1)

    print(f"Loaded {len(passages)} passages from {len(args.input)} file(s)")

    # Shuffle
    if args.shuffle:
        random.seed(args.seed)
        random.shuffle(passages)
        print(f"Shuffled with seed={args.seed}")

    # Write
    if args.split is not None:
        train_path, val_path, n_train, n_val = write_split(
            passages, args.output_prefix, args.split, args.seed,
        )
        print(f"Train: {n_train} passages -> {train_path}")
        print(f"Val:   {n_val} passages -> {val_path}")

        # Token counts
        if args.tokenizer:
            train_text = train_path.read_text()
            val_text = val_path.read_text()
            train_tokens = count_tokens(train_text, args.tokenizer)
            val_tokens = count_tokens(val_text, args.tokenizer)
            if train_tokens is not None:
                print(f"Train tokens: {train_tokens:,}")
                print(f"Val tokens:   {val_tokens:,}")
                print(f"Total tokens: {train_tokens + val_tokens:,}")
    else:
        out_path = write_single(passages, args.output_prefix)
        print(f"Wrote {len(passages)} passages -> {out_path}")

        if args.tokenizer:
            text = out_path.read_text()
            n_tokens = count_tokens(text, args.tokenizer)
            if n_tokens is not None:
                print(f"Total tokens: {n_tokens:,}")


if __name__ == "__main__":
    main()
