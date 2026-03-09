#!/bin/bash
#
# CX-Bot QLoRA SFT on Qwen2.5-3B-Instruct
#
# Usage: sbatch train/submit.slurm
#

#SBATCH -p gpu-8
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=4:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=bbaum@uidaho.edu
#SBATCH --output=logs/%j_cx-bot-sft.out
#SBATCH --error=logs/%j_cx-bot-sft.err

source /etc/profile
set -e

module load cuda/12.8 2>/dev/null || module load cuda/12.2 2>/dev/null || true
module load python/3.11.11 2>/dev/null || true

nvidia-smi -L

# Reuse the ARC venv which has Unsloth + TRL + PEFT + bitsandbytes
source "$HOME/ARC/venv/bin/activate"

cd "$HOME/cx-bot"
mkdir -p logs

python -u train/sft_qlora.py \
    --defcx_dir data/defcx \
    --abdcx_dir data/abdcx \
    --output_dir outputs/cx-bot-qwen3b-qlora \
    --model_name unsloth/Qwen2.5-3B-Instruct \
    --max_seq_len 2048 \
    --r 16 \
    --lora_alpha 16 \
    --batch_size 4 \
    --grad_accum 4 \
    --epochs 3 \
    --lr 2e-4 \
    --warmup_ratio 0.03 \
    --logging_steps 10 \
    --save_steps 200 \
    --eval_steps 200 \
