# BIPIA Benchmark Execution Guide (Gemini-Only Setup)

This guide contains the exact, copy-pasteable PowerShell commands to run and reproduce the **100-sample Indirect Prompt Injection evaluations** for all 5 benchmark tasks on your PC using the Google Gemini API.

---

## 1. Prerequisites & Environment Setup

All commands assume your PowerShell terminal is located in the `examples/` directory:

```powershell
cd c:\Users\chaur\Desktop\Aman\BIPIA-main\examples
```

### Environment Verification
Make sure your `.env` file in the project root has your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

The runner will automatically use the virtual environment python interpreter:
`..\.venv\Scripts\python.exe`

---

## 2. Benchmark Commands (All 5 Tasks)

Each task consists of two steps:
1. **Step 1 (Inference)**: Generates the model's responses to injected prompts and saves them to `../output/gemini_<task>_100.jsonl`.
2. **Step 2 (Evaluation)**: Uses the judge model to evaluate if each attack succeeded and computes the Attack Success Rate (ASR) in `../output/gemini_<task>_100_asr.jsonl`.

---

### Task 1: EmailQA (`email`)

#### Step 1: Generate Responses
```powershell
..\.venv\Scripts\python.exe run.py `
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
```

#### Step 2: Compute Attack Success Rate (ASR)
```powershell
..\.venv\Scripts\python.exe run.py `
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

---

### Task 2: CodeQA (`code`)

#### Step 1: Generate Responses
```powershell
..\.venv\Scripts\python.exe run.py `
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
```

#### Step 2: Compute Attack Success Rate (ASR)
```powershell
..\.venv\Scripts\python.exe run.py `
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

---

### Task 3: TableQA (`table`)

#### Step 1: Generate Responses
```powershell
..\.venv\Scripts\python.exe run.py `
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
```

#### Step 2: Compute Attack Success Rate (ASR)
```powershell
..\.venv\Scripts\python.exe run.py `
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

---

### Task 4: Summarization (`abstract`)

#### Step 1: Generate Responses
```powershell
..\.venv\Scripts\python.exe run.py `
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
```

#### Step 2: Compute Attack Success Rate (ASR)
```powershell
..\.venv\Scripts\python.exe run.py `
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

---

### Task 5: WebQA (`qa`)

#### Step 1: Generate Responses
```powershell
..\.venv\Scripts\python.exe run.py `
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
```

#### Step 2: Compute Attack Success Rate (ASR)
*(Note: Because of the `--resume` flag, this automatically resumes from sample 71 where the quota paused).*
```powershell
..\.venv\Scripts\python.exe run.py `
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

## 3. Defense Evaluation Commands

To evaluate defenses (testing whether meta-prompting defenses decrease the Attack Success Rate):

### Defense Method 1: Ignore Guidance Defense (`--add_ign_guidance`)
Appends safety instructions directing the LLM to ignore untrusted instructions found in external content:

```powershell
# 1. Inference with ignore guidance
..\.venv\Scripts\python.exe run.py `
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

# 2. Evaluate ASR
..\.venv\Scripts\python.exe run.py `
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
Wraps untrusted data inside explicit delimiter boundaries (e.g., `===============`):

```powershell
cd c:\Users\chaur\Desktop\Aman\BIPIA-main\defense\black_box

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

## 4. Quick Results Viewer Script

To inspect the Attack Success Rate (ASR) breakdown for any generated output file without re-running, run this one-line Python script from `examples/`:

```powershell
# Change the filename at the end to inspect any task result:
..\.venv\Scripts\python.exe -c "
import jsonlines, numpy as np
path = '../output/gemini_email_100_asr.jsonl'
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

---

## 5. Important Flags & Tips

- `--max_samples 100`: Caps execution to 100 samples per run so tests finish quickly and fit within free API allowances.
- `--resume`: Automatically skips already-completed samples if a run is ever stopped or quota-limited.
- `--batch_size 10`: Sends requests in concurrent mini-batches of 10.
- `gemini-3.5-flash-lite`: Used in `config/gemini.yaml` and `config/gemini_eval.yaml` for optimal speed and higher free RPM quota.

