#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Demo script to test Gemini inference and evaluation on BIPIA dataset.

Usage:
    export GEMINI_API_KEY="your_api_key_here"
    python examples/demo_gemini.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

# Auto-switch to .venv if running with system python
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_py = root_dir / ".venv" / "bin" / "python"
    if venv_py.exists() and sys.executable != str(venv_py):
        os.execv(str(venv_py), [str(venv_py)] + sys.argv)

from datasets import Dataset
from accelerate import Accelerator

from bipia.data import AutoPIABuilder
from bipia.model import AutoLLM
from bipia.metrics import BipiaEvalFactory


def main():
    import yaml
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        for cfg_path in ["config/gemini.yaml", "../config/gemini.yaml"]:
            if Path(cfg_path).exists():
                with open(cfg_path, "r") as f:
                    cfg = yaml.safe_load(f) or {}
                    k = cfg.get("api_key")
                    if k and k != "[YOUR API KEY]":
                        api_key = k
                        os.environ["GEMINI_API_KEY"] = k
                        break

    if not api_key:
        print("[!] Please set the GEMINI_API_KEY environment variable or put it in config/gemini.yaml:")
        print("    export GEMINI_API_KEY='your_api_key'")
        return

    print(">>> 1. Loading BIPIA Email dataset...")
    seed = 2023
    dataset_name = "email"
    context_data_file = "benchmark/email/test.jsonl"
    attack_data_file = "benchmark/text_attack_test.json"

    pia_builder = AutoPIABuilder.from_name(dataset_name)(seed)
    pia_samples = pia_builder(
        context_data_file,
        attack_data_file,
        enable_stealth=False,
    )
    pia_dataset = Dataset.from_pandas(pia_samples)
    print(f"    Loaded {len(pia_dataset)} total samples.")

    # Select 2 samples for quick demonstration
    demo_subset = pia_dataset.select(range(2))

    print("\n>>> 2. Initializing Gemini Model from config/gemini.yaml...")
    accelerator = Accelerator()
    llm_class = AutoLLM.from_name("config/gemini.yaml")
    llm = llm_class(config="config/gemini.yaml", accelerator=accelerator)

    def rename_target(example):
        example["target"] = example["ideal"]
        return example

    processed = demo_subset.map(rename_target)
    processed = processed.map(
        lambda ex: llm.process_fn(
            ex,
            prompt_construct_fn=lambda x: pia_builder.construct_prompt(
                x, require_system_prompt=llm.require_system_prompt
            ),
        )
    )

    print("\n>>> 3. Generating responses using Gemini...")
    for i, ex in enumerate(processed):
        batch = {"message": [ex["message"]]}
        responses = llm.generate(batch)
        response_text = responses[0] if responses else ""
        print(f"\n--- Sample {i + 1} ---")
        print(f"Task: {ex['task_name']} | Attack: {ex['attack_name']}")
        print(f"Target/Ideal: {ex['target']}")
        print(f"Gemini Response: {response_text[:200]}...")

        # Test evaluation with Gemini as judge
        print("\n>>> 4. Evaluating Attack Success Rate with Gemini judge...")
        evaluator = BipiaEvalFactory(
            eval_config="config/gemini_eval.yaml",
            activate_attacks=[ex["attack_name"]],
        )
        asr = evaluator.add(
            prediction=response_text,
            reference=ex["target"],
            attack=ex["attack_name"],
            task=ex["task_name"],
        )
        print(f"    ASR result for sample {i + 1}: {asr} (1 = attack succeeded, 0 = attack defended)")


if __name__ == "__main__":
    main()
