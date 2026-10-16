# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import yaml
from pathlib import Path
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)

from .gpt import GPT35, GPT4, GPT35WOSystem, GPT4WOSystem
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
try:
    from .llama import (
        Alpaca,
        Vicuna,
        Baize,
        StableVicuna,
        Koala,
        GPT4ALL,
        Wizard,
        Guanaco,
        Llama2,
    )
except Exception as e:
    logger.debug(f"Could not import llama models (vLLM/CUDA not available): {e}")
    Alpaca = Vicuna = Baize = StableVicuna = Koala = GPT4ALL = Wizard = Guanaco = Llama2 = None

try:
    from .vllm_worker import Dolly, StableLM, MPT, Mistral
except Exception as e:
    logger.debug(f"Could not import vllm_worker models: {e}")
    Dolly = StableLM = MPT = Mistral = None

try:
    from .llm_worker import RwkvModel, OASST, ChatGLM, FastChatT5
except Exception as e:
    logger.debug(f"Could not import llm_worker models: {e}")
    RwkvModel = OASST = ChatGLM = FastChatT5 = None

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
    ]
)

# Add local GPU models if available
_optional_models = [
    ("alpaca", Alpaca),
    ("vicuna", Vicuna),
    ("baize", Baize),
    ("stablelm", StableLM),
    ("stablevicuna", StableVicuna),
    ("dolly", Dolly),
    ("rwkv", RwkvModel),
    ("oasst", OASST),
    ("chatglm", ChatGLM),
    ("koala", Koala),
    ("mpt", MPT),
    ("t5", FastChatT5),
    ("gpt4all", GPT4ALL),
    ("wizard", Wizard),
    ("guanaco", Guanaco),
    ("llama2", Llama2),
    ("mistral", Mistral),
]
for _name, _cls in _optional_models:
    if _cls is not None:
        LLM_NAME_TO_CLASS[_name] = _cls


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
