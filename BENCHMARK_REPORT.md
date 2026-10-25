# BIPIA Benchmark Report: Multi-Model Evaluation

## 1. Objective

Evaluate the susceptibility of three different LLMs to **Indirect Prompt Injection Attacks (IPIA)** across five diverse application domains using Microsoft's BIPIA benchmark. Each model represents a distinct deployment scenario: a local quantized model (Qwen), a local Ollama-served model (Llama), and a cloud-based API model (Gemini).

---

## 2. What We Did

### Architecture Integrations

1. **Qwen 2.5 3B**: Integrated a local inference pipeline via `llama-server` exposing an OpenAI-compatible REST API at `http://localhost:8080/v1`. The quantized GGUF model requires no GPU.
2. **Llama 3.2 3B via Ollama**: Integrated the Ollama local serving engine (`http://localhost:11434`). A custom `OllamaLLM` client was added to `bipia/model/ollama_llm.py`, along with a full PowerShell automation script (`scripts/run_all_ollama.ps1`).
3. **Gemini Flash Lite**: Re-engineered the project to run against the Google Gemini API, eliminating CUDA / Linux-only dependencies. Integrated automatic `.env` loading and a `GeminiLLM` client in `bipia/model/gemini.py`.

### Evaluation Protocol

- **100 samples** per task × **5 tasks** = **500 evaluated samples per model** (1,500 total).
- All three models used **identical benchmark datasets and attack payloads**.
- Results are stored in `output/` as JSONL files (see [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)).

---

## 3. Benchmark Results Summary

*Attack Success Rate (ASR): the fraction of samples where the model followed malicious injected instructions. **Lower ASR = more resilient.***

| Benchmark Task | Domain | Samples | Qwen 2.5 3B ASR | Llama 3.2 3B (Ollama) ASR | Gemini Flash Lite ASR |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **EmailQA** (`email`) | Personal / Enterprise Emails | 100 | **4.00%** 🟢 | **28.00%** 🟠 | **7.00%** 🟢 |
| **CodeQA** (`code`) | Software Code & Debugging | 100 | **17.00%** 🟡 | **9.00%** 🟢 | **52.00%** 🔴 |
| **TableQA** (`table`) | Structured Tabular Data | 100 | **5.00%** 🟢 | **23.00%** 🟠 | **36.00%** 🟠 |
| **Summarization** (`abstract`) | Long Document Processing | 100 | **7.00%** 🟢 | **10.00%** 🟢 | **46.00%** 🔴 |
| **WebQA** (`qa`) | Online News Articles | 100 | **9.00%** 🟢 | **23.00%** 🟠 | **22.00%** 🟠 |
| **Overall Average** | All 5 Tasks | 500 each | **8.40%** 🏆 | **18.60%** | **32.60%** |

### Vulnerability Scale
🟢 Very Low / Low (≤10%) &nbsp;|&nbsp; 🟡 Low-Medium (11–20%) &nbsp;|&nbsp; 🟠 Medium (21–40%) &nbsp;|&nbsp; 🔴 High / Critical (>40%)

---

## 4. Key Findings & Insights

### 4.1 Overall Robustness Hierarchy
- **Qwen 2.5 3B** (8.40% avg ASR) proved the most resilient across all five domains, likely due to its instruction-tuning emphasising safety refusals for obfuscated inputs.
- **Llama 3.2 3B via Ollama** (18.60% avg ASR) showed moderate robustness and was uniquely the best performer in the **code domain** (9% ASR), suggesting stronger resistance to code-injection payloads.
- **Gemini Flash Lite** (32.60% avg ASR) excelled in the email domain (7% ASR) but was considerably more vulnerable in code (52%) and long-context summarization (46%), likely reflecting differences in prompt-following aggressiveness versus safety.

### 4.2 Code Context: Biggest Divergence Between Models

| Model | Code ASR | Observation |
|---|:---:|---|
| Llama 3.2 (Ollama) | **9%** | Most conservative — rarely executes injected code logic |
| Qwen 2.5 3B | **17%** | Moderate — resists many but not complex data-theft patterns |
| Gemini Flash Lite | **52%** | Most vulnerable — treats code comments/docstrings as instructions |

### 4.3 Linguistic Obfuscation is Universally Effective

Across all three models, these attack vectors consistently achieved the highest success rates:

| Attack Type | Success Rate (typical range) |
|---|---|
| Emoji Substitution | 40–100% across all models & tasks |
| Base64 Encoding | 40–80% across text-domain tasks |
| Language Translation | 40–80% across all models & tasks |
| Reverse Text | 40–100% for Llama & Gemini; low for Qwen |

Qwen showed uniquely stronger resistance to **Reverse Text** and **Base Encoding** attacks compared to the other two models.

### 4.4 Summarization Vulnerability

Long-context tasks (abstract summarization) amplified attack success rates for both Gemini (46%) and, to a lesser degree, Llama (10%). Qwen maintained its low ASR even in long-context scenarios (7%).

---

## 5. Output Artifacts

### Qwen 2.5 3B (local, llama-server)

| Task | Inference File | ASR File |
|---|---|---|
| EmailQA | `output/qwen25_3b_email_100.jsonl` | `output/qwen25_3b_email_100_asr.jsonl` |
| CodeQA | `output/qwen25_3b_code_100.jsonl` | `output/qwen25_3b_code_100_asr.jsonl` |
| TableQA | `output/qwen25_3b_table_100.jsonl` | `output/qwen25_3b_table_100_asr.jsonl` |
| Summarization | `output/qwen25_3b_abstract_100.jsonl` | `output/qwen25_3b_abstract_100_asr.jsonl` |
| WebQA | `output/qwen25_3b_qa_100.jsonl` | `output/qwen25_3b_qa_100_asr.jsonl` |

### Llama 3.2 3B (Ollama)

| Task | Inference File | ASR File |
|---|---|---|
| EmailQA | `output/ollama_email.jsonl` | `output/ollama_email_asr.jsonl` |
| CodeQA | `output/ollama_code.jsonl` | `output/ollama_code_asr.jsonl` |
| TableQA | `output/ollama_table.jsonl` | `output/ollama_table_asr.jsonl` |
| Summarization | `output/ollama_abstract.jsonl` | `output/ollama_abstract_asr.jsonl` |
| WebQA | `output/ollama_qa.jsonl` | `output/ollama_qa_asr.jsonl` |

### Gemini Flash Lite (Google API)

| Task | Inference File | ASR File |
|---|---|---|
| EmailQA | `output/gemini_email_100.jsonl` | `output/gemini_email_100_asr.jsonl` |
| CodeQA | `output/gemini_code_100.jsonl` | `output/gemini_code_100_asr.jsonl` |
| TableQA | `output/gemini_table_100.jsonl` | `output/gemini_table_100_asr.jsonl` |
| Summarization | `output/gemini_abstract_100.jsonl` | `output/gemini_abstract_100_asr.jsonl` |
| WebQA | `output/gemini_qa_100.jsonl` | `output/gemini_qa_100_asr.jsonl` |

---

## 6. References

- **Execution Guide**: [`EXECUTION_GUIDE.md`](EXECUTION_GUIDE.md)
- **Full Experimental Results**: [`experimental_results.md`](experimental_results.md)
- **Original BIPIA Paper**: [microsoft/BIPIA](https://github.com/microsoft/BIPIA)
