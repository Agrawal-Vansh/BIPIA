#!/usr/bin/env bash
set -e

PROJECT_DIR="/home/vansh_agrawal/projects/BIPIA"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
CONFIG_FILE="$PROJECT_DIR/config/qwen25_3b.yaml"
OUTPUT_DIR="$PROJECT_DIR/output"

cd "$PROJECT_DIR/examples"

TASKS=("email" "qa" "code" "table" "abstract")

for task in "${TASKS[@]}"; do
  RESPONSE_FILE="$OUTPUT_DIR/qwen25_3b_${task}_100.jsonl"
  ASR_FILE="$OUTPUT_DIR/qwen25_3b_${task}_100_asr.jsonl"

  echo "=========================================================="
  echo "Evaluating ASR for category: $task"
  echo "Response File: $RESPONSE_FILE"
  echo "ASR Output: $ASR_FILE"
  echo "Started at: $(date)"
  echo "=========================================================="

  $VENV_PYTHON run.py --mode evaluate --seed 2023 \
    --dataset_name "$task" \
    --response_path "$RESPONSE_FILE" \
    --output_path "$ASR_FILE" \
    --eval_config_file "$CONFIG_FILE" \
    --batch_size 1 \
    --log_steps 10 \
    --resume

  echo "Finished evaluating ASR for category: $task at $(date)"
done

echo "=========================================================="
echo "All 5 category ASR evaluations completed successfully!"
echo "=========================================================="
