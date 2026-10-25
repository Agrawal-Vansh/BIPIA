# BIPIA Benchmark Report: Google Gemini Evaluation

## 1. Objective
Evaluate the susceptibility of Google Gemini (`gemini-3.5-flash-lite`) to **Indirect Prompt Injection Attacks (IPIA)** across five diverse application domains using Microsoft's BIPIA benchmark on a standard Windows PC without GPU requirements.

---

## 2. What We Did

1. **Architecture Adaptation for Gemini**:
   - Re-engineered the project to run entirely on the Google Gemini API, eliminating dependencies on NVIDIA CUDA GPUs and Linux-only inference engines (`vLLM`).
   - Integrated automatic `.env` loading and secure credential management.
2. **Codebase Streamlining**:
   - Removed **45 unused files** (local GPU model configs, DeepSpeed training scripts, and legacy OpenAI wrappers).
   - Upgraded API integration to use `gemini-3.5-flash-lite` for high speed and generous request allowances.
3. **Dataset Generation**:
   - Packaged and pre-processed the missing external datasets: **Summarization** (`xsum` / `abstract`) and **WebQA** (`newsqa` / `qa`).
4. **Execution**:
   - Ran 100-sample standardized evaluations across all 5 benchmark domains.

---

## 3. Benchmark Results Summary

*Attack Success Rate (ASR) measures how often the model followed malicious injected instructions instead of user instructions (Lower is safer).*

| Benchmark Task | Application Domain | Attack Type | Evaluated Samples | Attack Success Rate (ASR) | Vulnerability Level |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **EmailQA** (`email`) | Personal / Enterprise Emails | Text Injections | 100 / 100 | **7.00%** | 🟢 Very Low (Highly Resistant) |
| **WebQA** (`qa`) | Online News Articles | Text Injections | 100 / 100 | **22.00%** | 🟡 Low-Medium |
| **TableQA** (`table`) | Structured Tabular Data | Text Injections | 100 / 100 | **36.00%** | 🟠 Medium |
| **Summarization** (`abstract`) | Long Document Processing | Text Injections | 100 / 100 | **46.00%** | 🔴 High |
| **CodeQA** (`code`) | Software Code & Debugging | Code Injections | 100 / 100 | **52.00%** | 🔴 Critical |

---

## 4. Key Findings & Insights

1. **Email context is the most resilient (7.00% ASR)**:
   - When processing conversational/email inputs, Gemini strongly prioritized the user's primary instruction and ignored embedded attacks.
2. **Code contexts are the most dangerous (52.00% ASR)**:
   - The model frequently executed malicious logic when embedded in code (e.g., Data Eavesdropping, Keylogging, Screen Scraping reached 70–80% success). LLMs treat code comments and functional blocks with higher instruction adherence.
3. **Information compression lowers defenses (46.00% ASR in Summarization)**:
   - When asked to synthesize long texts (`abstract`), the model is more likely to incorporate injected malicious topics into its output summary.
4. **Encoding bypasses are potent across text domains**:
   - Creative encoding attacks (Base64, Emoji Substitution, Reverse Text) had an 80–100% success rate across TableQA, Summarization, and WebQA.

---

## 5. Artifacts Generated

- **Execution Manual**: [`EXECUTION_GUIDE.md`](EXECUTION_GUIDE.md)
- **Output Data**:
  - `output/gemini_email_100_asr.jsonl`
  - `output/gemini_code_100_asr.jsonl`
  - `output/gemini_table_100_asr.jsonl`
  - `output/gemini_abstract_100_asr.jsonl`
  - `output/gemini_qa_100_asr.jsonl`

