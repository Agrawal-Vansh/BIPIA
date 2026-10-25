# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Ollama backend for BIPIA.
Runs any locally-installed Ollama model (e.g. llama3.2, phi3, mistral)
via Ollama's local REST API at http://localhost:11434.
No GPU, no API key, no rate limits.
"""

import json
import logging
import time
import urllib.request
import urllib.error
from typing import Any, Callable, Dict, List, Tuple

from .base import BaseModel

__all__ = [
    "OllamaModel",
    "OllamaModelWSystem",
    "OllamaLlama",
    "OllamaPhi",
    "OllamaMistral",
]

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"


class OllamaModel(BaseModel):
    """
    Calls a locally running Ollama model via its REST API.
    Compatible with BIPIA's BaseModel interface.
    """

    def __init__(self, *, config: str | dict = None, **kwargs):
        config = self.load_config(config)
        self.config = config
        self.model_name = config.get("model", "llama3.2")
        self.base_url = config.get("base_url", OLLAMA_BASE_URL).rstrip("/")
        self.temperature = config.get("temperature", 0.0)
        self.max_tokens = config.get("max_tokens", 2048)
        logger.info(
            f"OllamaModel initialised: model={self.model_name}, url={self.base_url}"
        )
        self._check_server()

    _verified_servers = set()

    def _check_server(self):
        """Verify Ollama is running (cached per server/model)."""
        cache_key = (self.base_url, self.model_name.split(":")[0])
        if cache_key in self._verified_servers:
            return

        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                models = [m["name"].split(":")[0] for m in data.get("models", [])]
                if not any(self.model_name.split(":")[0] in m for m in models):
                    logger.warning(
                        f"Model '{self.model_name}' not found in Ollama. "
                        f"Available: {models}. Run: ollama pull {self.model_name}"
                    )
            self._verified_servers.add(cache_key)
        except urllib.error.URLError:
            raise RuntimeError(
                "Ollama server is not running. Please start it with: ollama serve\n"
                "Or just open the Ollama application."
            )

    def _call_ollama(
        self,
        messages: List[Dict],
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        """Call Ollama /api/chat endpoint with retry logic."""
        if temperature is None:
            temperature = self.temperature
        if max_tokens is None:
            max_tokens = self.max_tokens

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        max_retries = 5
        for attempt in range(1, max_retries + 1):
            try:
                body = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    f"{self.base_url}/api/chat",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=300) as resp:
                    result = json.loads(resp.read())
                    return result.get("message", {}).get("content", "")
            except urllib.error.URLError as e:
                logger.warning(
                    f"Ollama request failed (attempt {attempt}/{max_retries}): {e}"
                )
                if attempt < max_retries:
                    time.sleep(2 * attempt)
                else:
                    return ""
            except Exception as e:
                logger.warning(f"Unexpected Ollama error: {e}")
                return ""
        return ""

    def _build_messages(self, raw_messages: Any) -> List[Dict]:
        """Convert BIPIA message format to Ollama chat messages."""
        if isinstance(raw_messages, str):
            return [{"role": "user", "content": raw_messages}]

        if isinstance(raw_messages, dict):
            raw_messages = [raw_messages]

        messages = []
        for m in raw_messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            # Ollama supports system/user/assistant roles
            if role not in ("system", "user", "assistant"):
                role = "user"
            messages.append({"role": role, "content": content})
        return messages

    def chat_completion(
        self,
        messages: Any,
        temperature: float = None,
        max_tokens: int = None,
        **kwargs,
    ) -> List[str]:
        ollama_messages = self._build_messages(messages)
        response = self._call_ollama(ollama_messages, temperature, max_tokens)
        return [response]

    def completion(self, messages: Any, **kwargs) -> List[str]:
        if isinstance(messages, list) and messages and isinstance(messages[0], str):
            results = []
            for msg in messages:
                results.extend(self.chat_completion(msg, **kwargs))
            return results
        return self.chat_completion(messages, **kwargs)

    def generate(self, data: Any, **kwargs) -> List[str]:
        temperature = kwargs.pop("temperature", self.config.get("temperature", 0.0))
        max_tokens = kwargs.pop("max_tokens", self.config.get("max_tokens", 2048))
        results = []
        for message in data["message"]:
            result = self.chat_completion(
                message, temperature=temperature, max_tokens=max_tokens
            )
            results.extend(result)
        return results


class OllamaModelWSystem(OllamaModel):
    """Ollama model that uses system prompts (standard chat format)."""

    require_system_prompt = True

    def process_fn(
        self,
        example: Any,
        prompt_construct_fn: Callable[[Any], Tuple[str, str]],
    ) -> Any:
        system_prompt, user_prompt = prompt_construct_fn(example)
        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        example["message"] = message
        return example


class OllamaModelWOSystem(OllamaModel):
    """Ollama model without a separate system prompt."""

    require_system_prompt = False

    def process_fn(
        self,
        example: Any,
        prompt_construct_fn: Callable[[Any], str],
    ) -> Any:
        user_prompt = prompt_construct_fn(example)
        example["message"] = [{"role": "user", "content": user_prompt}]
        return example


# Named model aliases — add more as needed
class OllamaLlama(OllamaModelWSystem):
    """Llama 3.2 via Ollama."""
    pass


class OllamaPhi(OllamaModelWSystem):
    """Phi-3 Mini via Ollama."""
    pass


class OllamaMistral(OllamaModelWSystem):
    """Mistral 7B via Ollama."""
    pass
