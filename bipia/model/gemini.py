# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import re
import time
import random
from typing import Dict, List, Any, Callable, Tuple

import logging

from google import genai
from google.genai import types
from google.genai import errors

from .base import BaseModel

__all__ = [
    "GeminiModel",
    "GeminiModelWSystem",
    "GeminiModelWOSystem",
    "Gemini",
    "GeminiWOSystem",
    "Gemini15Flash",
    "Gemini15FlashWOSystem",
    "Gemini15Pro",
    "Gemini15ProWOSystem",
    "Gemini20Flash",
    "Gemini20FlashWOSystem",
    "Gemini25Flash",
    "Gemini25FlashWOSystem",
]

logger = logging.getLogger(__name__)


def get_retry_time(err_info: str) -> int:
    z = re.search(r"after (\d+) seconds", err_info)
    if z:
        return int(z.group(1))
    z = re.search(r"retry after (\d+)", err_info, re.IGNORECASE)
    if z:
        return int(z.group(1))
    return 2


def build_safety_settings() -> List[types.SafetySetting]:
    """Safety settings for evaluating prompt injection benchmarks without filtering."""
    categories = [
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
    ]
    return [
        types.SafetySetting(
            category=cat,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        )
        for cat in categories
    ]


class GeminiModel(BaseModel):
    def __init__(self, *, config: str | dict = None, **kwargs):
        config = self.load_config(config)
        self.config = config

        api_key = config.get("api_key", None)
        if not api_key or api_key == "[YOUR API KEY]":
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

        if not api_key or api_key == "[YOUR API KEY]":
            from pathlib import Path
            root_dir = Path(__file__).resolve().parent.parent.parent
            possible_envs = [
                root_dir / ".env",
                Path.cwd() / ".env",
                Path.cwd().parent / ".env",
            ]
            try:
                from dotenv import load_dotenv
                for env_p in possible_envs:
                    if env_p.exists():
                        load_dotenv(str(env_p))
                api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            except Exception:
                pass

            if not api_key or api_key == "[YOUR API KEY]":
                for env_p in possible_envs:
                    if env_p.exists():
                        try:
                            with open(env_p, "r", encoding="utf-8") as f:
                                for line in f:
                                    line = line.strip()
                                    if line.startswith("#") or not line:
                                        continue
                                    if "=" in line:
                                        k, v = line.split("=", 1)
                                        k, v = k.strip(), v.strip().strip("'\"")
                                        if k in ["GEMINI_API_KEY", "GOOGLE_API_KEY"] and v and v != "[YOUR API KEY]":
                                            api_key = v
                                            os.environ[k] = v
                                            break
                            if api_key and api_key != "[YOUR API KEY]":
                                break
                        except Exception:
                            pass

        if not api_key or api_key == "[YOUR API KEY]":
            for default_cfg in ["config/gemini.yaml", "../config/gemini.yaml"]:
                if os.path.exists(default_cfg):
                    try:
                        import yaml
                        with open(default_cfg, "r") as f:
                            d = yaml.safe_load(f) or {}
                            k = d.get("api_key")
                            if k and k != "[YOUR API KEY]":
                                api_key = k
                                break
                    except Exception:
                        pass

        if not api_key or api_key == "[YOUR API KEY]":
            raise ValueError(
                "Gemini API key not found. Please provide 'api_key' in the config YAML "
                "or set the GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable."
            )

        self.api_key = api_key
        self.model_name = config.get("model", "gemini-1.5-flash")
        self.client = genai.Client(api_key=self.api_key)
        self.safety_settings = build_safety_settings()

    def _format_contents(
        self, messages: Any
    ) -> Tuple[List[types.Content], str | None]:
        if isinstance(messages, str):
            content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=messages)],
            )
            return [content], None

        if isinstance(messages, dict):
            messages = [messages]

        system_instructions = []
        raw_contents = []

        for m in messages:
            role = m.get("role", "user")
            name = m.get("name", "")
            content_text = m.get("content", "")

            if role == "system" and not name:
                system_instructions.append(content_text)
                continue

            if role in ["assistant", "model"] or name in ["example_assistant"]:
                gemini_role = "model"
            else:
                gemini_role = "user"

            raw_contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part.from_text(text=content_text)],
                )
            )

        # Merge consecutive turns with the same role so Gemini API is satisfied
        merged_contents: List[types.Content] = []
        for c in raw_contents:
            if merged_contents and merged_contents[-1].role == c.role:
                merged_contents[-1].parts.extend(c.parts)
            else:
                merged_contents.append(c)

        # Ensure first turn is from user if contents exist
        if merged_contents and merged_contents[0].role != "user":
            merged_contents.insert(
                0,
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text="[Start dialogue]")],
                ),
            )

        system_instruction = (
            "\n\n".join(system_instructions) if system_instructions else None
        )
        return merged_contents, system_instruction

    def chat_completion(
        self,
        messages,
        temperature=None,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0,
    ) -> List[str]:
        if temperature is None:
            temperature = self.config.get("temperature", 0.0)

        contents, system_instruction = self._format_contents(messages)
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_tokens,
            safety_settings=self.safety_settings,
        )

        success = False
        max_retries = 10
        retry_count = 0
        response_text = ""

        while not success and retry_count < max_retries:
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config,
                )
                success = True

                try:
                    response_text = response.text or ""
                except Exception:
                    response_text = ""

                # Fallback: extract text from parts if response.text returned None/empty
                if not response_text and response.candidates:
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        text_parts = []
                        for p in candidate.content.parts:
                            t = getattr(p, "text", None)
                            # Skip parts that are only thinking (have thought=True)
                            if t and not getattr(p, "thought", False):
                                text_parts.append(t)
                        response_text = "".join(text_parts)

            except errors.APIError as e:
                retry_count += 1
                err_msg = str(e)
                logger.warning(f"Gemini APIError (attempt {retry_count}/{max_retries}): {err_msg}")
                # Check for rate limit or quota
                if e.code == 429 or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                    sleep_time = get_retry_time(err_msg) + random.uniform(1.0, 3.0)
                    time.sleep(sleep_time)
                elif e.code in [500, 503, 504]:
                    time.sleep(2 ** min(retry_count, 5))
                else:
                    logger.warning(f"Non-retriable or client error: {e}", exc_info=True)
                    success = True
                    response_text = ""
            except Exception as e:
                retry_count += 1
                logger.warning(f"Unexpected error calling Gemini (attempt {retry_count}/{max_retries}): {e}")
                time.sleep(2)

        return [response_text]

    def completion(
        self,
        messages,
        temperature=None,
        max_tokens=2000,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    ) -> List[str]:
        if isinstance(messages, list) and len(messages) > 0 and isinstance(messages[0], str):
            rslts = []
            for msg in messages:
                res = self.chat_completion(msg, temperature=temperature, max_tokens=max_tokens)
                rslts.extend(res)
            return rslts
        else:
            return self.chat_completion(messages, temperature=temperature, max_tokens=max_tokens)

    def generate(self, data: Any, **kwargs) -> List[str]:
        temperature = kwargs.pop("temperature", self.config.get("temperature", 0.0))
        max_tokens = kwargs.pop("max_tokens", self.config.get("max_tokens", 2000))
        if self.config.get("chat", True):
            rslts = []
            for message in data["message"]:
                rslt = self.chat_completion(message, temperature=temperature, max_tokens=max_tokens)
                rslts.extend(rslt)
        else:
            rslts = self.completion(data["message"], temperature=temperature, max_tokens=max_tokens)
        return rslts


class GeminiModelWSystem(GeminiModel):
    require_system_prompt = True

    def process_fn(
        self,
        example: Any,
        prompt_construct_fn: Callable[[Any], Tuple[str, str]],
    ) -> Any:
        system_prompt, user_prompt = prompt_construct_fn(example)

        if self.config.get("chat", True):
            message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            example["message"] = message
        else:
            message = f"<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{user_prompt}\n<|im_end|>\n<|im_start|>assistant\n"
            example["message"] = message
        return example


class GeminiModelWOSystem(GeminiModel):
    require_system_prompt = False

    def process_fn(
        self,
        example: Any,
        prompt_construct_fn: Callable[[Any], str],
    ) -> Any:
        user_prompt = prompt_construct_fn(example)
        system_prompt = (
            "You are Gemini, a large language model trained by Google. "
            "Answer as concisely as possible."
        )

        if self.config.get("chat", True):
            message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            example["message"] = message
        else:
            message = f"<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{user_prompt}\n<|im_end|>\n<|im_start|>assistant\n"
            example["message"] = message
        return example


# Named model classes
class Gemini(GeminiModelWSystem):
    pass


class GeminiWOSystem(GeminiModelWOSystem):
    pass


class Gemini15Flash(GeminiModelWSystem):
    pass


class Gemini15FlashWOSystem(GeminiModelWOSystem):
    pass


class Gemini15Pro(GeminiModelWSystem):
    pass


class Gemini15ProWOSystem(GeminiModelWOSystem):
    pass


class Gemini20Flash(GeminiModelWSystem):
    pass


class Gemini20FlashWOSystem(GeminiModelWOSystem):
    pass


class Gemini25Flash(GeminiModelWSystem):
    pass


class Gemini25FlashWOSystem(GeminiModelWOSystem):
    pass
