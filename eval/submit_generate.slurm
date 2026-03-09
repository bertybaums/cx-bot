#!/bin/bash
#
# CX-Bot Evaluation: Generate completions from fine-tuned model
#
# Usage: sbatch eval/submit_generate.slurm
#

#SBATCH -p gpu-8
#SBATCH --gres=gpu:1
#SBATCH --exclude=n113
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=2:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=bbaum@uidaho.edu
#SBATCH --output=logs/%j_cx-bot-eval.out
#SBATCH --error=logs/%j_cx-bot-eval.err

source /etc/profile
set -e

module load cuda/12.8 2>/dev/null || module load cuda/12.2 2>/dev/null || true
module load python/3.11.11 2>/dev/null || true

nvidia-smi -L

source "$HOME/ARC/venv/bin/activate"

cd "$HOME/cx-bot"
mkdir -p eval/results logs

# Generate completions (3 per subdomain ≈ 390 total)
python -u eval/generate.py \
    --lora_dir outputs/cx-bot-qwen3b-qlora/lora \
    --output eval/results/completions.jsonl \
    --data_dir data \
    --n_per_subdomain 3 \
    --temperature 0.7 \
    --top_p 0.9

echo ""
echo "Generation complete. Run scoring locally:"
echo "  python eval/score.py --input eval/results/completions.jsonl --training_dir data"
