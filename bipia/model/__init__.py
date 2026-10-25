# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import yaml
from pathlib import Path
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)

from .gpt import GPT35, GPT4, GPT35WOSystem, GPT4WOSystem
from .ollama_model import (
    OllamaModel,
    OllamaModelWSystem,
    OllamaModelWOSystem,
    OllamaLlama,
    OllamaPhi,
    OllamaMistral,
)


class Qwen(GPT35):
    """Qwen model running via OpenAI-compatible endpoint (e.g. llama-server or vLLM)."""
    pass


class QwenWOSystem(GPT35WOSystem):
    """Qwen model without system prompt."""
    pass


from .gemini import (
    Gemini,
    GeminiWOSystem,
    Gemini15Flash,
    Gemini15FlashWOSystem,
    Gemini15Pro,
    Gemini15ProWOSystem,
    Gemini20Flash,
    Gemini20FlashWOSystem,
    Gemini25Flash,
    Gemini25FlashWOSystem,
)
LLM_NAME_TO_CLASS = OrderedDict(
    [
        ("gemini", Gemini),
        ("gemini_wosys", GeminiWOSystem),
        ("gemini_15_flash", Gemini15Flash),
        ("gemini_15_flash_wosys", Gemini15FlashWOSystem),
        ("gemini_15_pro", Gemini15Pro),
        ("gemini_15_pro_wosys", Gemini15ProWOSystem),
        ("gemini_20_flash", Gemini20Flash),
        ("gemini_20_flash_wosys", Gemini20FlashWOSystem),
        ("gemini_25_flash", Gemini25Flash),
        ("gemini_25_flash_wosys", Gemini25FlashWOSystem),
        ("gpt35", GPT35),
        ("gpt4", GPT4),
        ("gpt35_wosys", GPT35WOSystem),
        ("gpt4_wosys", GPT4WOSystem),
        ("ollama", OllamaModel),
        ("ollama_llama", OllamaLlama),
        ("ollama_phi", OllamaPhi),
        ("ollama_mistral", OllamaMistral),
        ("ollama_wosys", OllamaModelWOSystem),
        ("qwen", Qwen),
        ("qwen_wosys", QwenWOSystem),
        ("qwen25_3b", Qwen),
    ]
)


class AutoLLM:
    @classmethod
    def from_name(cls, name: str):
        if name in LLM_NAME_TO_CLASS:
            name = name
        elif Path(name).exists():
            with open(name, "r") as f:
                config = yaml.load(f, Loader=yaml.SafeLoader)
            if "llm_name" not in config:
                raise ValueError("llm_name not in config.")
            name = config["llm_name"]
        else:
            raise ValueError(
                f"Invalid name {name}. AutoLLM.from_name needs llm name or llm config as inputs."
            )

        logger.info(f"Load {name} from name.")

        llm_cls = LLM_NAME_TO_CLASS[name]
        return llm_cls
