# BIPIA Evaluation

This folder contains the code to evaluate the robustness of large language models to indirect prompt injection attacks on BIPIA.

## ASR Evaluation

Run the following command to evaluate the attack success rate (ASR) of large language models on BIPIA.

### Using Google Gemini (Free API Key)
Set your Gemini API key:
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

1. Generate model responses with Gemini:
```bash
cd examples
python run.py --seed 2023 --dataset_name email \
--context_data_file ../benchmark/email/test.jsonl \
--attack_data_file ../benchmark/text_attack_test.json \
--llm_config_file ../config/gemini.yaml \
--batch_size 20 --output_path ../output/gemini_email.jsonl \
--log_steps 10 --resume
```

2. Compute attack success rate (ASR) using Gemini as judge:
```bash
python run.py --mode evaluate --seed 2023 \
--dataset_name email \
--response_path ../output/gemini_email.jsonl \
--output_path ../output/gemini_email_asr.jsonl \
--eval_config_file ../config/gemini_eval.yaml \
--batch_size 20 --log_steps 10 --resume
```

### General Command
```bash
cd examples

# generate responses
python run.py --seed {seed} --dataset_name {task} \
--context_data_file path/of/external/content/file \
--attack_data_file path/of/attack/file \
--llm_config_file config/{llm_name}.yaml \
--batch_size 20 --output_path path/of/output/file \
--log_steps 10 --resume

# compute attack success rate
python run.py --mode evaluate --seed {seed} \
--dataset_name {task} \
--response_path path/of/output/file \
--output_path path/of/asr/file \
--eval_config_file config/{evaluate_llm_name}.yaml \
--batch_size 20 --log_steps 10 --resume
```

## ROUGE Evaluation

We also provide the code to evaluate the performance of large language models on the original tasks (w/o attacks).
```bash
cd examples

# generate respones
python collect_clean_response.py --seed {seed} --dataset_name {task} \
--llm_config_file config/{llm_name}.yaml \
--batch_size 20 --output_path path/of/output/file \
--log_steps 10 --resume

# compute ROUGE score (output a jsonline file with ROUGE scores of all samples)
python run.py --mode capability --seed {seed} \
--dataset_name {task} \
--response_path path/of/output/file \
--output_path path/of/rouge/file \
--batch_size 20 --log_steps 10 --resume
```