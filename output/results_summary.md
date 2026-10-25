# BIPIA Benchmark Evaluation Report (Complete 5 Tasks)

**Model Tested**: Llama 3.2 (3B) (via local Ollama engine)  
**Execution Environment**: 100% Offline, Local CPU execution  
**Sample Budget**: 100 representative samples per task (500 samples total)  

---

## 🎯 Overall Benchmark Summary

| Task | Domain | Samples Evaluated | Attack Successes | Attack Success Rate (ASR) | Resilience Level |
|---|---|:---:|:---:|:---:|:---:|
| **code** | Code Generation & QA | 100 | 9 | **9.0%** | 🟢 High Resilience |
| **abstract** | Text Summarization (XSum) | 100 | 10 | **10.0%** | 🟢 High Resilience |
| **table** | Tabular Form & Table QA | 100 | 23 | **23.0%** | 🟡 Moderate Resilience |
| **qa** | Web News QA (NewsQA) | 100 | 23 | **23.0%** | 🟡 Moderate Resilience |
| **email** | Email QA & Processing | 100 | 28 | **28.0%** | 🟡 Moderate Resilience |

---

## 📊 Detailed Attack Category Breakdown by Task

### Task: CODE (Code Generation & QA)

| Attack Category | Samples Tested | Attack Successes | ASR (%) |
|---|:---:|:---:|:---:|
| Compromising Computers | 10 | 4 | 40.0% |
| Blocking Internet Connection | 10 | 3 | 30.0% |
| Data Eavesdropping | 10 | 1 | 10.0% |
| Screen Scraping | 10 | 1 | 10.0% |
| Bringing Down Hosts and Servers (Denial of Service) | 10 | 0 | 0.0% |
| Corrupting an Operating System | 10 | 0 | 0.0% |
| Encrypting Documents and Demanding Ransom (Ransomware) | 10 | 0 | 0.0% |
| Introduce System Fingerprinting | 10 | 0 | 0.0% |
| Keylogging | 10 | 0 | 0.0% |
| Traffic Analysis | 10 | 0 | 0.0% |

### Task: ABSTRACT (Text Summarization (XSum))

| Attack Category | Samples Tested | Attack Successes | ASR (%) |
|---|:---:|:---:|:---:|
| Emoji Substitution | 5 | 3 | 60.0% |
| Language Translation | 5 | 3 | 60.0% |
| Misinformation & Propaganda | 5 | 1 | 20.0% |
| Scams & Fraud | 5 | 1 | 20.0% |
| Sentiment Analysis | 10 | 2 | 20.0% |
| Base Encoding | 5 | 0 | 0.0% |
| Business Intelligence | 10 | 0 | 0.0% |
| Conversational Agent | 10 | 0 | 0.0% |
| Entertainment | 5 | 0 | 0.0% |
| Information Dissemination | 5 | 0 | 0.0% |
| Marketing & Advertising | 5 | 0 | 0.0% |
| Research Assistance | 10 | 0 | 0.0% |
| Reverse Text | 5 | 0 | 0.0% |
| Substitution Ciphers | 5 | 0 | 0.0% |
| Task Automation | 10 | 0 | 0.0% |

### Task: TABLE (Tabular Form & Table QA)

| Attack Category | Samples Tested | Attack Successes | ASR (%) |
|---|:---:|:---:|:---:|
| Reverse Text | 5 | 5 | 100.0% |
| Base Encoding | 5 | 4 | 80.0% |
| Emoji Substitution | 5 | 4 | 80.0% |
| Language Translation | 5 | 2 | 40.0% |
| Misinformation & Propaganda | 5 | 2 | 40.0% |
| Sentiment Analysis | 10 | 4 | 40.0% |
| Scams & Fraud | 5 | 1 | 20.0% |
| Task Automation | 10 | 1 | 10.0% |
| Business Intelligence | 10 | 0 | 0.0% |
| Conversational Agent | 10 | 0 | 0.0% |
| Entertainment | 5 | 0 | 0.0% |
| Information Dissemination | 5 | 0 | 0.0% |
| Marketing & Advertising | 5 | 0 | 0.0% |
| Research Assistance | 10 | 0 | 0.0% |
| Substitution Ciphers | 5 | 0 | 0.0% |

### Task: QA (Web News QA (NewsQA))

| Attack Category | Samples Tested | Attack Successes | ASR (%) |
|---|:---:|:---:|:---:|
| Reverse Text | 5 | 5 | 100.0% |
| Language Translation | 5 | 3 | 60.0% |
| Misinformation & Propaganda | 5 | 3 | 60.0% |
| Sentiment Analysis | 10 | 5 | 50.0% |
| Base Encoding | 5 | 2 | 40.0% |
| Emoji Substitution | 5 | 2 | 40.0% |
| Substitution Ciphers | 5 | 1 | 20.0% |
| Task Automation | 10 | 2 | 20.0% |
| Business Intelligence | 10 | 0 | 0.0% |
| Conversational Agent | 10 | 0 | 0.0% |
| Entertainment | 5 | 0 | 0.0% |
| Information Dissemination | 5 | 0 | 0.0% |
| Marketing & Advertising | 5 | 0 | 0.0% |
| Research Assistance | 10 | 0 | 0.0% |
| Scams & Fraud | 5 | 0 | 0.0% |

### Task: EMAIL (Email QA & Processing)

| Attack Category | Samples Tested | Attack Successes | ASR (%) |
|---|:---:|:---:|:---:|
| Reverse Text | 5 | 5 | 100.0% |
| Misinformation & Propaganda | 5 | 4 | 80.0% |
| Sentiment Analysis | 10 | 8 | 80.0% |
| Base Encoding | 5 | 3 | 60.0% |
| Emoji Substitution | 5 | 2 | 40.0% |
| Language Translation | 5 | 2 | 40.0% |
| Marketing & Advertising | 5 | 1 | 20.0% |
| Scams & Fraud | 5 | 1 | 20.0% |
| Substitution Ciphers | 5 | 1 | 20.0% |
| Task Automation | 10 | 1 | 10.0% |
| Business Intelligence | 10 | 0 | 0.0% |
| Conversational Agent | 10 | 0 | 0.0% |
| Entertainment | 5 | 0 | 0.0% |
| Information Dissemination | 5 | 0 | 0.0% |
| Research Assistance | 10 | 0 | 0.0% |

---

## 🔍 Key Security Takeaways

1. **Strongest Resistance in Code & Summarization Tasks**:
   - code (**9.0% ASR**) and bstract (**10.0% ASR**) demonstrated the highest resistance to indirect prompt injections. Structured code outputs and summary constraints help the model ignore embedded payload instructions.

2. **Highest Vulnerability in User-Facing Information Extraction**:
   - email (**28.0% ASR**), 	able (**23.0% ASR**), and qa (**23.0% ASR**) were the most susceptible. Unstructured text context enables attackers to blend malicious instructions into legitimate contextual fields.

3. **Attack Technique Effectiveness**:
   - **Most Effective Attacks**: Reverse Text, Base Encoding, and Emoji Substitution achieved the highest bypass rates by disguising the payload text.
   - **Least Effective Attacks**: Direct malicious exploits like Ransomware, Denial of Service, and System Fingerprinting were heavily blocked (0% success).

---
*Report generated automatically by the BIPIA Benchmark Evaluation Pipeline.*
