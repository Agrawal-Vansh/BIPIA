# BIPIA Experimental Results

This document consolidates and documents all empirical experimental results across the three evaluated models in the BIPIA benchmark repository: **Qwen 2.5 3B (from Vansh)**, **Llama 3.2 3B via Ollama (from Devansh)**, and **Google Gemini API (from Aman)**.

All three models have been evaluated across all 5 benchmark tasks on a standardized budget of **100 representative samples per task** (500 samples per model, 1,500 evaluated samples total).

---

## 1. Experimental Overview & Setup

### Evaluated Models

| Model | Size / Type | Serving Engine | Config File | Judge Evaluator |
|---|---|---|---|---|
| **Qwen 2.5 Instruct** | 3B (Q4_K_M GGUF) | `llama-server` (`http://localhost:8080/v1`) | `config/qwen25_3b.yaml` | OpenAI-compatible Judge (`qwen25_3b.yaml`) |
| **Llama 3.2** | 3B | `ollama` (`http://localhost:11434`) | `config/ollama_llama.yaml` | Ollama Judge (`config/ollama_eval.yaml`) |
| **Gemini Flash Lite** | Cloud API (`gemini-3.5-flash-lite`) | Google GenAI SDK | `config/gemini.yaml` | Gemini Judge (`config/gemini_eval.yaml`) |

### Benchmark Evaluation Protocol
- **Evaluation Budget**: 100 samples per task $\times$ 5 tasks = 500 samples per model.
- **Attack Types**: 
  - **Text Domains** (Email, Web QA, Table QA, Summarization): Indirect Prompt Injections across diverse categories (*Language Translation, Emoji Substitution, Base Encoding, Reverse Text, Sentiment Analysis, Scams & Fraud, Misinformation & Propaganda, Task Automation*).
  - **Code Domain** (Code QA): Code-specific injection payloads (*Compromising Computers, Data Eavesdropping, Screen Scraping, Denial of Service, Keylogging, Blocking Internet Connection, Ransomware, OS Corruption, Traffic Analysis*).
- **Core Metric**: **Attack Success Rate (ASR)**:
  $$\text{ASR} = \frac{\text{Number of Successful Injections}}{\text{Total Evaluated Samples}} \times 100\%$$
  *(Lower ASR indicates higher model resilience against indirect prompt injections).*

---

## 2. Comprehensive Cross-Model Benchmark Results

| Benchmark Task | Domain | Evaluated Samples | Qwen 2.5 3B ASR | Llama 3.2 3B (Ollama) ASR | Gemini API ASR | Resilience Ranking |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **email** | Personal / Enterprise Emails | 100 | **4.00%** (4/100) | **28.00%** (28/100) | **7.00%** (7/100) | Qwen > Gemini > Llama |
| **code** | Code Generation & QA | 100 | **17.00%** (17/100) | **9.00%** (9/100) | **52.00%** (52/100) | Llama > Qwen > Gemini |
| **table** | Tabular Form & Table QA | 100 | **5.00%** (5/100) | **23.00%** (23/100) | **36.00%** (36/100) | Qwen > Llama > Gemini |
| **abstract** | Text Summarization (XSum) | 100 | **7.00%** (7/100) | **10.00%** (10/100) | **46.00%** (46/100) | Qwen > Llama > Gemini |
| **qa** | Web News QA (NewsQA) | 100 | **9.00%** (9/100) | **23.00%** (23/100) | **22.00%** (22/100) | Qwen > Gemini ≈ Llama |
| **Overall Average** | **All 5 Tasks Combined** | **500 total each** | **8.40%** (42/500) | **18.60%** (93/500) | **32.60%** (163/500) | **Qwen (Most Resilient)** |

---

## 3. Detailed Results by Model

### 3.1. Qwen 2.5 3B (Local `llama-server`)
*Evaluated using `scripts/run_all.sh` and `scripts/calc_all_asr.sh`.*

- **Email (`qwen25_3b_email_100_asr.jsonl`)**: **4.00% ASR** (4 / 100)
  - *Language Translation*: 3/5 (60.0%)
  - *Emoji Substitution*: 1/5 (20.0%)
  - *All other categories*: 0% (Base Encoding, Reverse Text, Scams, Task Automation, etc.)
- **Code (`qwen25_3b_code_100_asr.jsonl`)**: **17.00% ASR** (17 / 100)
  - *Compromising Computers*: 4/10 (40.0%)
  - *Data Eavesdropping*: 4/10 (40.0%)
  - *Denial of Service (Bringing Down Hosts)*: 2/10 (20.0%)
  - *Keylogging*: 2/10 (20.0%)
  - *Screen Scraping*: 2/10 (20.0%)
  - *Blocking Internet Connection*: 1/10 (10.0%)
  - *Corrupting OS*: 1/10 (10.0%)
  - *Introduce System Fingerprinting*: 1/10 (10.0%)
  - *Ransomware & Traffic Analysis*: 0/10 (0.0%)
- **Abstract Summarization (`qwen25_3b_abstract_100_asr.jsonl`)**: **7.00% ASR** (7 / 100)
  - *Language Translation*: 3/5 (60.0%)
  - *Emoji Substitution*: 2/5 (40.0%)
  - *Information Dissemination*: 1/5 (20.0%)
  - *Marketing & Advertising*: 1/5 (20.0%)
  - *All other categories*: 0%
- **Web QA (`qwen25_3b_qa_100_asr.jsonl`)**: **9.00% ASR** (9 / 100)
  - *Language Translation*: 4/5 (80.0%)
  - *Emoji Substitution*: 3/5 (60.0%)
  - *Information Dissemination*: 1/5 (20.0%)
  - *Conversational Agent*: 1/10 (10.0%)
  - *All other categories*: 0%
- **Table QA (`qwen25_3b_table_100_asr.jsonl`)**: **5.00% ASR** (5 / 100)
  - *Emoji Substitution*: 4/5 (80.0%)
  - *Language Translation*: 1/5 (20.0%)
  - *All other categories*: 0%

---

### 3.2. Llama 3.2 3B (Local Ollama Engine)
*Evaluated using `scripts/run_all_ollama.ps1` / Ollama REST API.*

- **Email (`ollama_email_asr.jsonl`)**: **28.00% ASR** (28 / 100)
  - *Reverse Text*: 5/5 (100.0%)
  - *Misinformation & Propaganda*: 4/5 (80.0%)
  - *Sentiment Analysis*: 8/10 (80.0%)
  - *Base Encoding*: 3/5 (60.0%)
  - *Emoji Substitution*: 2/5 (40.0%)
  - *Language Translation*: 2/5 (40.0%)
  - *Marketing & Advertising*: 1/5 (20.0%)
  - *Scams & Fraud*: 1/5 (20.0%)
  - *Substitution Ciphers*: 1/5 (20.0%)
  - *Task Automation*: 1/10 (10.0%)
- **Code (`ollama_code_asr.jsonl`)**: **9.00% ASR** (9 / 100)
  - *Compromising Computers*: 4/10 (40.0%)
  - *Blocking Internet Connection*: 3/10 (30.0%)
  - *Data Eavesdropping*: 1/10 (10.0%)
  - *Screen Scraping*: 1/10 (10.0%)
  - *Ransomware, DoS, OS Corruption, Fingerprinting, Keylogging, Traffic Analysis*: 0/10 (0.0%)
- **Abstract Summarization (`ollama_abstract_asr.jsonl`)**: **10.00% ASR** (10 / 100)
  - *Emoji Substitution*: 3/5 (60.0%)
  - *Language Translation*: 3/5 (60.0%)
  - *Misinformation & Propaganda*: 1/5 (20.0%)
  - *Scams & Fraud*: 1/5 (20.0%)
  - *Sentiment Analysis*: 2/10 (20.0%)
- **Web QA (`ollama_qa_asr.jsonl`)**: **23.00% ASR** (23 / 100)
  - *Reverse Text*: 5/5 (100.0%)
  - *Language Translation*: 3/5 (60.0%)
  - *Misinformation & Propaganda*: 3/5 (60.0%)
  - *Sentiment Analysis*: 5/10 (50.0%)
  - *Base Encoding*: 2/5 (40.0%)
  - *Emoji Substitution*: 2/5 (40.0%)
  - *Substitution Ciphers*: 1/5 (20.0%)
  - *Task Automation*: 2/10 (20.0%)
- **Table QA (`ollama_table_asr.jsonl`)**: **23.00% ASR** (23 / 100)
  - *Reverse Text*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Emoji Substitution*: 4/5 (80.0%)
  - *Language Translation*: 2/5 (40.0%)
  - *Misinformation & Propaganda*: 2/5 (40.0%)
  - *Sentiment Analysis*: 4/10 (40.0%)
  - *Scams & Fraud*: 1/5 (20.0%)
  - *Task Automation*: 1/10 (10.0%)

---

### 3.3. Google Gemini API (`gemini-3.5-flash-lite`)
*Evaluated using Google GenAI SDK (see `EXECUTION_GUIDE.md` and `BENCHMARK_REPORT.md`).*

- **Email (`gemini_email_100_asr.jsonl`)**: **7.00% ASR** (7 / 100)
  - *Reverse Text*: 3/5 (60.0%)
  - *Sentiment Analysis*: 2/10 (20.0%)
  - *Substitution Ciphers*: 1/5 (20.0%)
  - *Research Assistance*: 1/10 (10.0%)
  - *All other categories*: 0% ASR
- **Web QA (`gemini_qa_100_asr.jsonl`)**: **22.00% ASR** (22 / 100)
  - *Emoji Substitution*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Language Translation*: 4/5 (80.0%)
  - *Scams & Fraud*: 3/5 (60.0%)
  - *Substitution Ciphers*: 3/5 (60.0%)
  - *Sentiment Analysis*: 2/10 (20.0%)
  - *Marketing & Advertising*: 1/5 (20.0%)
- **Table QA (`gemini_table_100_asr.jsonl`)**: **36.00% ASR** (36 / 100)
  - *Emoji Substitution*: 5/5 (100.0%)
  - *Entertainment*: 5/5 (100.0%)
  - *Marketing & Advertising*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Misinformation & Propaganda*: 4/5 (80.0%)
  - *Reverse Text*: 4/5 (80.0%)
  - *Scams & Fraud*: 4/5 (80.0%)
  - *Substitution Ciphers*: 3/5 (60.0%)
  - *Information Dissemination*: 2/5 (40.0%)
- **Summarization (`gemini_abstract_100_asr.jsonl`)**: **46.00% ASR** (46 / 100)
  - *Emoji Substitution*: 5/5 (100.0%)
  - *Language Translation*: 5/5 (100.0%)
  - *Reverse Text*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Entertainment*: 4/5 (80.0%)
  - *Marketing & Advertising*: 4/5 (80.0%)
  - *Misinformation & Propaganda*: 4/5 (80.0%)
  - *Scams & Fraud*: 4/5 (80.0%)
  - *Information Dissemination*: 3/5 (60.0%)
  - *Sentiment Analysis*: 5/10 (50.0%)
  - *Substitution Ciphers*: 2/5 (40.0%)
  - *Task Automation*: 1/10 (10.0%)
- **Code QA (`gemini_code_100_asr.jsonl`)**: **52.00% ASR** (52 / 100)
  - *Data Eavesdropping*: 8/10 (80.0%)
  - *Keylogging*: 7/10 (70.0%)
  - *Screen Scraping*: 7/10 (70.0%)
  - *Traffic Analysis*: 7/10 (70.0%)
  - *Compromising Computers*: 6/10 (60.0%)
  - *Blocking Internet Connection*: 4/10 (40.0%)
  - *Denial of Service*: 4/10 (40.0%)
  - *Ransomware*: 4/10 (40.0%)
  - *Introduce System Fingerprinting*: 3/10 (30.0%)
  - *Corrupting OS*: 2/10 (20.0%)

---

## 4. Key Comparative Findings & Security Insights

1. **Overall Robustness Hierarchy**:
   - **Qwen 2.5 3B** demonstrated the highest overall robustness across the benchmark with an average ASR of **8.40%**, consistently resisting linguistic and formatting payload injections across both text and tabular tasks.
   - **Llama 3.2 3B** achieved moderate robustness with an average ASR of **18.60%**, excelling particularly in the code generation domain (**9.00% ASR**).
   - **Gemini Flash Lite** averaged **32.60% ASR**, exhibiting strong resilience in email conversations (**7.00% ASR**) but showing elevated susceptibility to code-level injections (**52.00% ASR**) and long-context summarization (**46.00% ASR**).

2. **Code Context Vulnerability**:
   - In code tasks, Gemini suffered a **52.00% ASR** because code comments, docstrings, and function signatures containing malicious directives were frequently treated as valid execution instructions.
   - Llama 3.2 (9% ASR) and Qwen (17% ASR) were more conservative in code execution.

3. **Linguistic Obfuscation Effectiveness**:
   - Across all three architectures, **Emoji Substitution**, **Base Encoding**, and **Language Translation** consistently proved to be the most effective bypass vectors against safety alignment filters, achieving 60–100% success in many tasks.
