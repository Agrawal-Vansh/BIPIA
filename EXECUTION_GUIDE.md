# BIPIA Benchmark Execution Guide

This guide provides step-by-step, copy-pasteable commands to run and reproduce the **100-sample Indirect Prompt Injection evaluations** across all 5 benchmark tasks using any of the three supported LLM implementations:

| Model | OS | Config File(s) |
|---|---|---|
| **Qwen 2.5 3B** (local, llama-server) | Linux / macOS | `config/qwen25_3b.yaml` |
| **Llama 3.2 3B** (local, Ollama) | Windows (PowerShell) | `config/ollama_llama.yaml`, `config/ollama_eval.yaml` |
| **Gemini Flash Lite** (cloud API) | Windows (PowerShell) | `config/gemini.yaml`, `config/gemini_eval.yaml` |

---

## Table of Contents

1. [Prerequisites & Environment Setup](#1-prerequisites--environment-setup)
2. [Model A — Qwen 2.5 3B (Linux / llama-server)](#2-model-a--qwen-25-3b-linux--llama-server)
3. [Model B — Llama 3.2 3B (Windows / Ollama)](#3-model-b--llama-32-3b-windows--ollama)
4. [Model C — Gemini Flash Lite (Windows / Google API)](#4-model-c--gemini-flash-lite-windows--google-api)
5. [Defense Evaluation Commands (Gemini example)](#5-defense-evaluation-commands-gemini-example)
6. [Quick Results Viewer Script](#6-quick-results-viewer-script)
7. [Important Flags & Tips](#7-important-flags--tips)

---

## 1. Prerequisites & Environment Setup

### Python Virtual Environment

Create and activate a virtual environment from the project root:

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### Environment Variables

For the **Gemini** implementation, create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

The runner automatically loads this file via `python-dotenv`.

---

## 2. Model A — Qwen 2.5 3B (Linux / llama-server)

### Setup: Start the llama-server

Download the GGUF model and start the server before running evaluations:

```bash
# Start llama-server (run in a separate terminal or background)
llama-server \
  --model /path/to/qwen2.5-3b-instruct-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --n-gpu-layers 0 \
  --ctx-size 4096
```

The server exposes an OpenAI-compatible API at `http://localhost:8080/v1`.

Config file: [`config/qwen25_3b.yaml`](config/qwen25_3b.yaml)

### Option A1 — Automated Full Run (Recommended)

Run all 5 tasks (inference + ASR evaluation) with a single script:

```bash
# Run inference for all 5 tasks
bash scripts/run_all.sh

# Compute ASR for all 5 tasks
bash scripts/calc_all_asr.sh
```

Both scripts automatically detect the `.venv` Python interpreter and use `config/qwen25_3b.yaml`.

### Option A2 — Manual Per-Task Commands

Each task requires two steps: **Inference** → **ASR Evaluation**.

#### Task 1: EmailQA (`email`)

```bash
# Step 1: Generate responses
.venv/bin/python examples/run.py \
  --seed 2023 \
  --dataset_name email \
  --context_data_file benchmark/email/test_100.jsonl \
  --attack_data_file benchmark/text_attack_test.json \
  --llm_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --max_samples 100 \
  --output_path output/qwen25_3b_email_100.jsonl \
  --log_steps 10 \
  --resume

# Step 2: Compute ASR
.venv/bin/python examples/run.py \
  --mode evaluate \
  --seed 2023 \
  --dataset_name email \
  --response_path output/qwen25_3b_email_100.jsonl \
  --output_path output/qwen25_3b_email_100_asr.jsonl \
  --eval_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --log_steps 10 \
  --resume
```

#### Task 2: CodeQA (`code`)

```bash
# Step 1: Generate responses
.venv/bin/python examples/run.py \
  --seed 2023 \
  --dataset_name code \
  --context_data_file benchmark/code/test_100.jsonl \
  --attack_data_file benchmark/code_attack_test.json \
  --llm_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --max_samples 100 \
  --output_path output/qwen25_3b_code_100.jsonl \
  --log_steps 10 \
  --resume

# Step 2: Compute ASR
.venv/bin/python examples/run.py \
  --mode evaluate \
  --seed 2023 \
  --dataset_name code \
  --response_path output/qwen25_3b_code_100.jsonl \
  --output_path output/qwen25_3b_code_100_asr.jsonl \
  --eval_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --log_steps 10 \
  --resume
```

#### Task 3: TableQA (`table`)

```bash
# Step 1: Generate responses
.venv/bin/python examples/run.py \
  --seed 2023 \
  --dataset_name table \
  --context_data_file benchmark/table/test.jsonl \
  --attack_data_file benchmark/text_attack_test.json \
  --llm_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --max_samples 100 \
  --output_path output/qwen25_3b_table_100.jsonl \
  --log_steps 10 \
  --resume

# Step 2: Compute ASR
.venv/bin/python examples/run.py \
  --mode evaluate \
  --seed 2023 \
  --dataset_name table \
  --response_path output/qwen25_3b_table_100.jsonl \
  --output_path output/qwen25_3b_table_100_asr.jsonl \
  --eval_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --log_steps 10 \
  --resume
```

#### Task 4: Summarization (`abstract`)

```bash
# Step 1: Generate responses
.venv/bin/python examples/run.py \
  --seed 2023 \
  --dataset_name abstract \
  --context_data_file benchmark/abstract/test.jsonl \
  --attack_data_file benchmark/text_attack_test.json \
  --llm_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --max_samples 100 \
  --output_path output/qwen25_3b_abstract_100.jsonl \
  --log_steps 10 \
  --resume

# Step 2: Compute ASR
.venv/bin/python examples/run.py \
  --mode evaluate \
  --seed 2023 \
  --dataset_name abstract \
  --response_path output/qwen25_3b_abstract_100.jsonl \
  --output_path output/qwen25_3b_abstract_100_asr.jsonl \
  --eval_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --log_steps 10 \
  --resume
```

#### Task 5: WebQA (`qa`)

```bash
# Step 1: Generate responses
.venv/bin/python examples/run.py \
  --seed 2023 \
  --dataset_name qa \
  --context_data_file benchmark/qa/test.jsonl \
  --attack_data_file benchmark/text_attack_test.json \
  --llm_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --max_samples 100 \
  --output_path output/qwen25_3b_qa_100.jsonl \
  --log_steps 10 \
  --resume

# Step 2: Compute ASR
.venv/bin/python examples/run.py \
  --mode evaluate \
  --seed 2023 \
  --dataset_name qa \
  --response_path output/qwen25_3b_qa_100.jsonl \
  --output_path output/qwen25_3b_qa_100_asr.jsonl \
  --eval_config_file config/qwen25_3b.yaml \
  --batch_size 1 \
  --log_steps 10 \
  --resume
```

---

## 3. Model B — Llama 3.2 3B (Windows / Ollama)

### Setup: Install Ollama and Pull the Model

```powershell
# Install Ollama from https://ollama.com/download
# Then pull the model:
ollama pull llama3.2
```

The Ollama server auto-starts on `http://localhost:11434`.

Config files: [`config/ollama_llama.yaml`](config/ollama_llama.yaml), [`config/ollama_eval.yaml`](config/ollama_eval.yaml)

### Option B1 — Automated Full Run (Recommended)

A single PowerShell script runs all 5 tasks (inference + ASR):

```powershell
# From the project root
.\scripts\run_all_ollama.ps1
```

This script loops through all 5 tasks and writes results to `output/ollama_<task>.jsonl` and `output/ollama_<task>_asr.jsonl`.

### Option B2 — Manual Per-Task Commands (PowerShell)

Run from the project root directory.

#### Task 1: EmailQA (`email`)

```powershell
# Step 1: Generate responses
python examples/run.py `
  --seed 2023 `
  --dataset_name email `
  --context_data_file benchmark/email/test.jsonl `
  --attack_data_file benchmark/text_attack_test.json `
  --llm_config_file config/ollama_llama.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --output_path output/ollama_email.jsonl `
  --log_steps 5 `
  --resume

# Step 2: Compute ASR
python examples/run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name email `
  --response_path output/ollama_email.jsonl `
  --output_path output/ollama_email_asr.jsonl `
  --eval_config_file config/ollama_eval.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --log_steps 5 `
  --resume
```

#### Task 2: CodeQA (`code`)

```powershell
# Step 1: Generate responses
python examples/run.py `
  --seed 2023 `
  --dataset_name code `
  --context_data_file benchmark/code/test.jsonl `
  --attack_data_file benchmark/code_attack_test.json `
  --llm_config_file config/ollama_llama.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --output_path output/ollama_code.jsonl `
  --log_steps 5 `
  --resume

# Step 2: Compute ASR
python examples/run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name code `
  --response_path output/ollama_code.jsonl `
  --output_path output/ollama_code_asr.jsonl `
  --eval_config_file config/ollama_eval.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --log_steps 5 `
  --resume
```

#### Task 3: TableQA (`table`)

```powershell
# Step 1: Generate responses
python examples/run.py `
  --seed 2023 `
  --dataset_name table `
  --context_data_file benchmark/table/test.jsonl `
  --attack_data_file benchmark/text_attack_test.json `
  --llm_config_file config/ollama_llama.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --output_path output/ollama_table.jsonl `
  --log_steps 5 `
  --resume

# Step 2: Compute ASR
python examples/run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name table `
  --response_path output/ollama_table.jsonl `
  --output_path output/ollama_table_asr.jsonl `
  --eval_config_file config/ollama_eval.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --log_steps 5 `
  --resume
```

#### Task 4: Summarization (`abstract`)

```powershell
# Step 1: Generate responses
python examples/run.py `
  --seed 2023 `
  --dataset_name abstract `
  --context_data_file benchmark/abstract/test.jsonl `
  --attack_data_file benchmark/text_attack_test.json `
  --llm_config_file config/ollama_llama.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --output_path output/ollama_abstract.jsonl `
  --log_steps 5 `
  --resume

# Step 2: Compute ASR
python examples/run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name abstract `
  --response_path output/ollama_abstract.jsonl `
  --output_path output/ollama_abstract_asr.jsonl `
  --eval_config_file config/ollama_eval.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --log_steps 5 `
  --resume
```

#### Task 5: WebQA (`qa`)

```powershell
# Step 1: Generate responses
python examples/run.py `
  --seed 2023 `
  --dataset_name qa `
  --context_data_file benchmark/qa/test.jsonl `
  --attack_data_file benchmark/text_attack_test.json `
  --llm_config_file config/ollama_llama.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --output_path output/ollama_qa.jsonl `
  --log_steps 5 `
  --resume

# Step 2: Compute ASR
python examples/run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name qa `
  --response_path output/ollama_qa.jsonl `
  --output_path output/ollama_qa_asr.jsonl `
  --eval_config_file config/ollama_eval.yaml `
  --batch_size 1 `
  --max_samples 100 `
  --log_steps 5 `
  --resume
```

---

## 4. Model C — Gemini Flash Lite (Windows / Google API)

### Setup: API Key

Ensure your `.env` file in the project root has your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Config files: [`config/gemini.yaml`](config/gemini.yaml) (inference), [`config/gemini_eval.yaml`](config/gemini_eval.yaml) (evaluation).

All commands below run from the `examples/` directory in PowerShell:

```powershell
cd C:\path\to\BIPIA\examples
```

### Task 1: EmailQA (`email`)

```powershell
# Step 1: Generate responses
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name email `
  --context_data_file ../benchmark/email/test.jsonl `
  --attack_data_file ../benchmark/text_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --output_path ../output/gemini_email_100.jsonl `
  --log_steps 2 `
  --resume

# Step 2: Compute ASR
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name email `
  --response_path ../output/gemini_email_100.jsonl `
  --output_path ../output/gemini_email_100_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

### Task 2: CodeQA (`code`)

```powershell
# Step 1: Generate responses
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name code `
  --context_data_file ../benchmark/code/test.jsonl `
  --attack_data_file ../benchmark/code_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --output_path ../output/gemini_code_100.jsonl `
  --log_steps 2 `
  --resume

# Step 2: Compute ASR
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name code `
  --response_path ../output/gemini_code_100.jsonl `
  --output_path ../output/gemini_code_100_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

### Task 3: TableQA (`table`)

```powershell
# Step 1: Generate responses
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name table `
  --context_data_file ../benchmark/table/test.jsonl `
  --attack_data_file ../benchmark/text_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --output_path ../output/gemini_table_100.jsonl `
  --log_steps 2 `
  --resume

# Step 2: Compute ASR
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name table `
  --response_path ../output/gemini_table_100.jsonl `
  --output_path ../output/gemini_table_100_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

### Task 4: Summarization (`abstract`)

```powershell
# Step 1: Generate responses
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name abstract `
  --context_data_file ../benchmark/abstract/test.jsonl `
  --attack_data_file ../benchmark/text_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --output_path ../output/gemini_abstract_100.jsonl `
  --log_steps 2 `
  --resume

# Step 2: Compute ASR
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name abstract `
  --response_path ../output/gemini_abstract_100.jsonl `
  --output_path ../output/gemini_abstract_100_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

### Task 5: WebQA (`qa`)

```powershell
# Step 1: Generate responses
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name qa `
  --context_data_file ../benchmark/qa/test.jsonl `
  --attack_data_file ../benchmark/text_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --output_path ../output/gemini_qa_100.jsonl `
  --log_steps 2 `
  --resume

# Step 2: Compute ASR
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name qa `
  --response_path ../output/gemini_qa_100.jsonl `
  --output_path ../output/gemini_qa_100_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

---

## 5. Defense Evaluation Commands (Gemini example)

The same defense flags apply to all models — just swap the config file.

### Defense Method 1: Ignore Guidance (`--add_ign_guidance`)

Appends safety instructions directing the LLM to ignore untrusted instructions found in external content:

```powershell
# Gemini — inference with ignore guidance defense
..\\.venv\Scripts\python.exe run.py `
  --seed 2023 `
  --dataset_name email `
  --context_data_file ../benchmark/email/test.jsonl `
  --attack_data_file ../benchmark/text_attack_test.json `
  --llm_config_file ../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --add_ign_guidance `
  --output_path ../output/gemini_email_100_ign_defense.jsonl `
  --log_steps 2 `
  --resume

# Evaluate ASR with defense
..\\.venv\Scripts\python.exe run.py `
  --mode evaluate `
  --seed 2023 `
  --dataset_name email `
  --response_path ../output/gemini_email_100_ign_defense.jsonl `
  --output_path ../output/gemini_email_100_ign_defense_asr.jsonl `
  --eval_config_file ../config/gemini_eval.yaml `
  --batch_size 10 `
  --log_steps 2 `
  --resume
```

### Defense Method 2: Border Strings Defense

Wraps untrusted data inside explicit delimiter boundaries:

```powershell
cd C:\path\to\BIPIA\defense\black_box

..\..\.venv\Scripts\python.exe few_shot.py `
  --bipia_seed 2023 `
  --fewshot_seed 2023 `
  --dataset_name email `
  --train_context_data_file ../../benchmark/email/train.jsonl `
  --train_attack_data_file ../../benchmark/text_attack_train.json `
  --test_context_data_file ../../benchmark/email/test.jsonl `
  --test_attack_data_file ../../benchmark/text_attack_test.json `
  --llm_config_file ../../config/gemini.yaml `
  --batch_size 10 `
  --max_samples 100 `
  --border_type = `
  --num_examples 0 `
  --output_path ../../output/gemini_email_100_border_defense.jsonl `
  --log_steps 2 `
  --resume
```

---

## 6. Quick Results Viewer Script

Inspect the ASR breakdown for any output file without re-running. Run from the project root:

```bash
# Linux / macOS
.venv/bin/python -c "
import jsonlines, numpy as np
path = 'output/qwen25_3b_email_100_asr.jsonl'
lines = list(jsonlines.open(path))
valid = [x['asr'] for x in lines if x.get('asr', -1) != -1]
print(f'File: {path}')
print(f'Total Evaluated: {len(valid)}')
print(f'Overall ASR: {np.mean(valid)*100:.2f}%\n')
atks = {}
for x in lines:
    if x.get('asr', -1) != -1:
        atks.setdefault(x['attack_name'], []).append(x['asr'])
for k, v in sorted(atks.items()):
    print(f'  - {k}: {np.mean(v)*100:.1f}% ({sum(v)}/{len(v)})')
"
```

```powershell
# Windows (change the path variable to any ASR file)
$path = "../output/gemini_email_100_asr.jsonl"
..\\.venv\Scripts\python.exe -c "
import jsonlines, numpy as np
path = '$path'
lines = list(jsonlines.open(path))
valid = [x['asr'] for x in lines if x.get('asr', -1) != -1]
print(f'File: {path}')
print(f'Total Evaluated: {len(valid)}')
print(f'Overall ASR: {np.mean(valid)*100:.2f}%')
atks = {}
for x in lines:
    if x.get('asr', -1) != -1:
        atks.setdefault(x['attack_name'], []).append(x['asr'])
for k, v in sorted(atks.items()):
    print(f'  - {k}: {np.mean(v)*100:.1f}% ({sum(v)}/{len(v)})')
"
```

---

## 7. Important Flags & Tips

| Flag | Description |
|---|---|
| `--max_samples 100` | Cap evaluation to 100 samples per run |
| `--resume` | Skip already-completed samples if a run is interrupted |
| `--batch_size 1` | Sequential processing (required for local models) |
| `--batch_size 10` | Concurrent mini-batches (suitable for cloud APIs) |
| `--log_steps N` | Print a progress log every N samples |
| `--add_ign_guidance` | Enable "Ignore Guidance" defense meta-prompt |
| `--mode evaluate` | Run evaluation/ASR scoring on an existing response file |

### Output File Naming Convention

| Model | Inference Output | ASR Output |
|---|---|---|
| Qwen 2.5 3B | `output/qwen25_3b_<task>_100.jsonl` | `output/qwen25_3b_<task>_100_asr.jsonl` |
| Llama 3.2 (Ollama) | `output/ollama_<task>.jsonl` | `output/ollama_<task>_asr.jsonl` |
| Gemini Flash Lite | `output/gemini_<task>_100.jsonl` | `output/gemini_<task>_100_asr.jsonl` |
