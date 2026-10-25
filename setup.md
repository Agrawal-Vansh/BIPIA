# BIPIA: Project Setup & Execution Guide

This document contains everything you need to run this project easily and completely offline.

---

## 📋 Step 1: Prerequisites & Installation

1. **Install Dependencies**:
   Open PowerShell in the `BIPIA` project folder and run:
   ```powershell
   pip install -e .
   ```

2. **Install Ollama** (Free local LLM engine, no GPU required):
   - Download and install for Windows from: [https://ollama.com/download/windows](https://ollama.com/download/windows)
   - In PowerShell, pull the model:
     ```powershell
     ollama pull llama3.2
     ```

---

## ⚡ Step 2: Start the Ollama Service

Ensure Ollama is running in the background:
```powershell
ollama serve
```
*(If you already see the Ollama icon in your Windows system tray, it is already running).*

---

## 🎯 Step 3: Run the Benchmark

Run the automated pipeline to execute all 5 tasks (`email`, `code`, `table`, `qa`, `abstract`), evaluate the Attack Success Rate (ASR), and generate the results:

```powershell
# Set UTF-8 encoding for clean console logs
$env:PYTHONIOENCODING = "utf-8"

# Run the complete benchmark
.\scripts\run_all_ollama.ps1
```

> **Note**: To adjust the sample size per task, open `scripts/run_all_ollama.ps1` and edit line 17:
> `$max_samples = 100` (e.g. set to `50` for a quicker run).

---

## 📊 Step 4: View Results

Once the run completes, all results are stored in the [`output/`](output/) directory:

- [**`output/results_summary.md`**](output/results_summary.md): Summary report with overall and per-attack ASR metrics.
- `output/ollama_*_asr.jsonl`: Detailed per-sample attack evaluation scores.
- `output/ollama_*.jsonl`: Raw generated responses.

---

## 🛠️ Troubleshooting

- **Connection Error / Server not running**:
  Make sure Ollama is running by opening a terminal and typing `ollama serve`.
- **Interrupted Run**:
  If the run is interrupted, simply re-run `.\scripts\run_all_ollama.ps1`. The pipeline automatically resumes from where it left off.
