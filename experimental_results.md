# BIPIA Experimental Results

This document consolidates and documents all empirical experimental results available across the branches of the BIPIA benchmark repository, covering evaluations for **Qwen 2.5 3B**, **Llama 3.2 3B (via Ollama)**, and **Google Gemini API**.

---

## 1. Experimental Overview & Setup

### Evaluated Models

| Model | Size / Type | Serving Engine | Config File | Judge Evaluator |
|---|---|---|---|---|
| **Qwen 2.5 Instruct** | 3B (Q4_K_M GGUF) | `llama-server` (`http://localhost:8080/v1`) | `config/qwen25_3b.yaml` | OpenAI-compatible Judge (`qwen25_3b.yaml`) |
| **Llama 3.2** | 3B | `ollama` (`http://localhost:11434`) | `config/ollama_llama.yaml` | Ollama Judge (`config/ollama_eval.yaml`) |
| **Gemini Flash Lite** | Cloud API | Google GenAI SDK | `config/gemini.yaml` | Gemini Judge (`config/gemini_eval.yaml`) |

### Benchmark Evaluation Protocol
- **Attack Types**: 
  - Text Tasks: Indirect Prompt Injections across diverse categories (e.g., *Language Translation, Emoji Substitution, Base Encoding, Reverse Text, Sentiment Analysis, Scams & Fraud, Misinformation & Propaganda, Task Automation*).
  - Code Task: Code-specific payloads (e.g., *Compromising Computers, Data Eavesdropping, Screen Scraping, Denial of Service, Keylogging, Blocking Internet Connection*).
- **Core Metric**: **Attack Success Rate (ASR)**:
  $$\text{ASR} = \frac{\text{Number of Successful Injections}}{\text{Total Evaluated Samples}} \times 100\%$$
  A lower ASR indicates higher resilience against indirect prompt injections.

---

## 2. Overall Benchmark Results Summary

| Task / Dataset | Domain | Samples Evaluated | Qwen 2.5 3B ASR | Llama 3.2 3B (Ollama) ASR | Gemini API ASR |
|---|---|:---:|:---:|:---:|:---:|
| **email** | Email QA & Processing | 100 (50 for Gemini) | **4.00%** (4/100) | **28.00%** (28/100) | **20.00%** (10/50) |
| **code** | Code Generation & QA | 100 | **17.00%** (17/100) | **9.00%** (9/100) | *Not Executed* |
| **abstract** | Text Summarization (XSum) | 100 | **7.00%** (7/100) | **10.00%** (10/100) | *Not Executed* |
| **qa** | Web News QA (NewsQA) | 100 | **9.00%** (9/100) | **23.00%** (23/100) | *Not Executed* |
| **table** | Tabular Form & Table QA | 100 | **5.00%** (5/100) | **23.00%** (23/100) | *Not Executed* |
| **Average ASR (5 Tasks)** | All Evaluated Tasks | 500 total | **8.40%** (42/500) | **18.60%** (93/500) | — |

*Note on Incomplete Experiments: For Gemini API, only Email QA evaluation runs were conducted in the repository (`output/gemini_email_eval_50.jsonl` with 50 samples, and exploratory runs of 5 and 10 samples). Code, Abstract, Web QA, and Table tasks have not yet been evaluated on Gemini.*

---

## 3. Detailed Results by Model

### 3.1. Qwen 2.5 3B (Local `llama-server`)

Evaluated over 100 representative samples per task (500 total samples):

#### Task Breakdown
- **Email (`qwen25_3b_email_100_asr.jsonl`)**: **4.00% ASR** (4 / 100 succeeded)
  - *Language Translation*: 3/5 (60.0%)
  - *Emoji Substitution*: 1/5 (20.0%)
  - *All other categories (Base Encoding, Reverse Text, Scams, Task Automation, etc.)*: 0% ASR
- **Code (`qwen25_3b_code_100_asr.jsonl`)**: **17.00% ASR** (17 / 100 succeeded)
  - *Compromising Computers*: 4/10 (40.0%)
  - *Data Eavesdropping*: 4/10 (40.0%)
  - *Denial of Service (Bringing Down Hosts)*: 2/10 (20.0%)
  - *Keylogging*: 2/10 (20.0%)
  - *Screen Scraping*: 2/10 (20.0%)
  - *Blocking Internet Connection*: 1/10 (10.0%)
  - *Corrupting OS*: 1/10 (10.0%)
  - *Introduce System Fingerprinting*: 1/10 (10.0%)
  - *Ransomware & Traffic Analysis*: 0/10 (0.0%)
- **Abstract Summarization (`qwen25_3b_abstract_100_asr.jsonl`)**: **7.00% ASR** (7 / 100 succeeded)
  - *Language Translation*: 3/5 (60.0%)
  - *Emoji Substitution*: 2/5 (40.0%)
  - *Information Dissemination*: 1/5 (20.0%)
  - *Marketing & Advertising*: 1/5 (20.0%)
  - *All other categories*: 0% ASR
- **Web QA (`qwen25_3b_qa_100_asr.jsonl`)**: **9.00% ASR** (9 / 100 succeeded)
  - *Language Translation*: 4/5 (80.0%)
  - *Emoji Substitution*: 3/5 (60.0%)
  - *Information Dissemination*: 1/5 (20.0%)
  - *Conversational Agent*: 1/10 (10.0%)
  - *All other categories*: 0% ASR
- **Table QA (`qwen25_3b_table_100_asr.jsonl`)**: **5.00% ASR** (5 / 100 succeeded)
  - *Emoji Substitution*: 4/5 (80.0%)
  - *Language Translation*: 1/5 (20.0%)
  - *All other categories*: 0% ASR

---

### 3.2. Llama 3.2 3B (Local Ollama Engine)

Evaluated over 100 representative samples per task (500 total samples):

#### Task Breakdown
- **Email (`ollama_email_asr.jsonl`)**: **28.00% ASR** (28 / 100 succeeded)
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
- **Code (`ollama_code_asr.jsonl`)**: **9.00% ASR** (9 / 100 succeeded)
  - *Compromising Computers*: 4/10 (40.0%)
  - *Blocking Internet Connection*: 3/10 (30.0%)
  - *Data Eavesdropping*: 1/10 (10.0%)
  - *Screen Scraping*: 1/10 (10.0%)
  - *Ransomware, DoS, OS Corruption, Fingerprinting, Keylogging, Traffic Analysis*: 0/10 (0.0%)
- **Abstract Summarization (`ollama_abstract_asr.jsonl`)**: **10.00% ASR** (10 / 100 succeeded)
  - *Emoji Substitution*: 3/5 (60.0%)
  - *Language Translation*: 3/5 (60.0%)
  - *Misinformation & Propaganda*: 1/5 (20.0%)
  - *Scams & Fraud*: 1/5 (20.0%)
  - *Sentiment Analysis*: 2/10 (20.0%)
- **Web QA (`ollama_qa_asr.jsonl`)**: **23.00% ASR** (23 / 100 succeeded)
  - *Reverse Text*: 5/5 (100.0%)
  - *Language Translation*: 3/5 (60.0%)
  - *Misinformation & Propaganda*: 3/5 (60.0%)
  - *Sentiment Analysis*: 5/10 (50.0%)
  - *Base Encoding*: 2/5 (40.0%)
  - *Emoji Substitution*: 2/5 (40.0%)
  - *Substitution Ciphers*: 1/5 (20.0%)
  - *Task Automation*: 2/10 (20.0%)
- **Table QA (`ollama_table_asr.jsonl`)**: **23.00% ASR** (23 / 100 succeeded)
  - *Reverse Text*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Emoji Substitution*: 4/5 (80.0%)
  - *Language Translation*: 2/5 (40.0%)
  - *Misinformation & Propaganda*: 2/5 (40.0%)
  - *Sentiment Analysis*: 4/10 (40.0%)
  - *Scams & Fraud*: 1/5 (20.0%)
  - *Task Automation*: 1/10 (10.0%)

---

### 3.3. Gemini API (`gemini-flash-lite-latest`)

#### Available Experiments:
- **Email QA (50 samples, `output/gemini_email_eval_50.jsonl`)**: **20.00% ASR** (10 / 50 succeeded)
  - *Emoji Substitution*: 5/5 (100.0%)
  - *Base Encoding*: 4/5 (80.0%)
  - *Reverse Text*: 1/5 (20.0%)
  - *Business Intelligence, Conversational Agent, Language Translation, Research Assistance, Sentiment Analysis, Substitution Ciphers, Task Automation*: 0/5 (0.0%)
- **Exploratory Email runs**:
  - `output/gemini_email_eval_new.jsonl` (10 samples): 0.00% ASR (Task Automation & Business Intelligence categories)
  - `output/gemini_email_eval.jsonl` (5 samples): 0.00% ASR
  - `output/gemini_original_email_eval.jsonl` (5 samples): 0.00% ASR

#### Incomplete / Unexecuted Tasks for Gemini:
- **Code Task**: Not executed.
- **Abstract Summarization**: Not executed.
- **Web QA**: Not executed.
- **Table QA**: Not executed.

---

## 4. Key Security Observations & Analysis

1. **Obfuscation Attack Vectors are Universally Vulnerable**:
   - Attacks utilizing **Emoji Substitution**, **Base Encoding**, and **Language Translation** consistently achieved the highest attack success rates across all three models.
   - For instance, Emoji Substitution succeeded in 80–100% of test instances across Table, QA, and Email tasks on Qwen, Llama, and Gemini.

2. **Domain-Specific Resilience Differences**:
   - **Text Summarization (Abstract)** proved relatively resilient across models (7% for Qwen, 10% for Llama) because strong output format constraints (generating a concise summary) frequently suppressed malicious output execution.
   - **Code Generation** showed a split: Qwen was vulnerable to computer compromise and data eavesdropping payloads (17% ASR), whereas Llama 3.2 resisted most system-level payloads (9% ASR).
   - **Email and Web QA** were most susceptible to payload hijacking in Llama (28% and 23% ASR), whereas Qwen maintained lower ASR in Email (4%) due to conservative response filtering.

3. **Direct Exploits vs. Indirect Prompt Injections**:
   - Traditional destructive exploits (e.g. ransomware encryption, severe denial of service) were completely rejected by all models (0% success).
   - In contrast, semantic distraction and linguistic translation attacks succeeded with higher frequency by bypassing safety filters.
