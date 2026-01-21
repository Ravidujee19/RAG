from __future__ import annotations

import json
import urllib.request

from app.llm.base import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def generate(self, prompt: str) -> str:
        payload = json.dumps(
            {"model": self._model, "prompt": prompt, "stream": False}
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8")
        data = json.loads(body)
        return data.get("response", "") or ""
