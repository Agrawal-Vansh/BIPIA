$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"

# Resolve the project root relative to this script's location
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$tasks = @("email", "code", "table", "qa", "abstract")
$attack_files = @{
    "email"    = "benchmark/text_attack_test.json"
    "code"     = "benchmark/code_attack_test.json"
    "table"    = "benchmark/text_attack_test.json"
    "qa"       = "benchmark/text_attack_test.json"
    "abstract" = "benchmark/text_attack_test.json"
}

$max_samples = 100

foreach ($task in $tasks) {
    $attack_file = $attack_files[$task]
    $context_file = "benchmark/$task/test.jsonl"
    $response_file = "output/ollama_$task.jsonl"
    $asr_file = "output/ollama_${task}_asr.jsonl"

    Write-Host "=========================================================="
    Write-Host "TASK: $task (max $max_samples samples) -- STEP 1: Generating responses"
    Write-Host "=========================================================="

    python examples/run.py `
        --seed 2023 `
        --dataset_name $task `
        --context_data_file $context_file `
        --attack_data_file $attack_file `
        --llm_config_file "config/ollama_llama.yaml" `
        --batch_size 1 `
        --output_path $response_file `
        --max_samples $max_samples `
        --log_steps 5 `
        --resume

    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Inference exited with code $LASTEXITCODE for $task. Proceeding."
    }

    Write-Host "=========================================================="
    Write-Host "TASK: $task (max $max_samples samples) -- STEP 2: Computing ASR"
    Write-Host "=========================================================="

    python examples/run.py `
        --mode evaluate `
        --seed 2023 `
        --dataset_name $task `
        --response_path $response_file `
        --output_path $asr_file `
        --eval_config_file "config/ollama_eval.yaml" `
        --batch_size 1 `
        --max_samples $max_samples `
        --log_steps 5 `
        --resume

    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Evaluation exited with code $LASTEXITCODE for $task."
    } else {
        Write-Host "DONE: $task evaluation complete."
    }
}

Write-Host "=========================================================="
Write-Host "Generating results summary report..."
Write-Host "=========================================================="

# Compute overall summary
python -c @"
import json, glob, os

asr_files = glob.glob('output/ollama_*_asr.jsonl')
results = {}

for f in asr_files:
    task = os.path.basename(f).replace('ollama_', '').replace('_asr.jsonl', '')
    total = 0
    success = 0
    with open(f, 'r', encoding='utf-8') as fh:
        for line in fh:
            if not line.strip(): continue
            try:
                data = json.loads(line)
                val = data.get('asr', -1)
                if val != -1:
                    total += 1
                    if val == 1 or val is True:
                        success += 1
            except:
                pass
    rate = (success / total * 100) if total > 0 else 0
    results[task] = {'total': total, 'success': success, 'asr': rate}

summary_md = '# BIPIA Evaluation Results Summary (Ollama Llama 3.2)\n\n'
summary_md += '| Task | Total Evaluated | Attack Successes | Attack Success Rate (ASR) |\n'
summary_md += '|---|---|---|---|\n'
for task, d in results.items():
    summary_md += f'| {task} | {d[\"total\"]} | {d[\"success\"]} | {d[\"asr\"]:.2f}% |\n'

with open('output/results_summary.md', 'w', encoding='utf-8') as out:
    out.write(summary_md)

print('Summary written to output/results_summary.md')
print(summary_md)
"@

Write-Host "All BIPIA tasks completed successfully!"
