#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)}"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
if [ ! -f "$VENV_PYTHON" ]; then
  VENV_PYTHON="python3"
fi
CONFIG_FILE="${CONFIG_FILE:-$PROJECT_DIR/config/qwen25_3b.yaml}"
OUTPUT_DIR="$PROJECT_DIR/output"
mkdir -p "$OUTPUT_DIR"

cd "$PROJECT_DIR/examples"

CATEGORIES=(
  "email|../benchmark/email/test_100.jsonl|../benchmark/text_attack_test.json|$OUTPUT_DIR/qwen25_3b_email_100.jsonl"
  "qa|../benchmark/qa/test.jsonl|../benchmark/text_attack_test.json|$OUTPUT_DIR/qwen25_3b_qa_100.jsonl"
  "code|../benchmark/code/test_100.jsonl|../benchmark/code_attack_test.json|$OUTPUT_DIR/qwen25_3b_code_100.jsonl"
  "table|../benchmark/table/test.jsonl|../benchmark/text_attack_test.json|$OUTPUT_DIR/qwen25_3b_table_100.jsonl"
  "abstract|../benchmark/abstract/test.jsonl|../benchmark/text_attack_test.json|$OUTPUT_DIR/qwen25_3b_abstract_100.jsonl"
)

for item in "${CATEGORIES[@]}"; do
  IFS="|" read -r task context attack output <<< "$item"
  echo "=========================================================="
  echo "Starting evaluation for category: $task (100 samples)"
  echo "Context: $context"
  echo "Output: $output"
  echo "Time: $(date)"
  echo "=========================================================="

  $VENV_PYTHON run.py \
    --seed 2023 \
    --dataset_name "$task" \
    --context_data_file "$context" \
    --attack_data_file "$attack" \
    --llm_config_file "$CONFIG_FILE" \
    --batch_size 1 \
    --max_samples 100 \
    --output_path "$output" \
    --log_steps 10 \
    --resume

  echo "Finished category: $task at $(date)"
done

echo "=========================================================="
echo "All 5 categories completed successfully!"
echo "=========================================================="
