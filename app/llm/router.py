from __future__ import annotations

from typing import Optional

from app.llm.base import LLMClient
from app.llm.cache import LLMCache


class FallbackLLM(LLMClient):
    def __init__(
        self,
        primary: LLMClient,
        fallback: LLMClient,
        cache: Optional[LLMCache] = None,
    ) -> None:
        self._primary = primary
        self._fallback = fallback
        self._cache = cache

    def generate(self, prompt: str) -> str:
        if self._cache:
            cached = self._cache.get(prompt)
            if cached is not None:
                return cached

        try:
            response = self._primary.generate(prompt)
        except Exception:
            response = self._fallback.generate(prompt)

        if self._cache:
            self._cache.set(prompt, response)
        return response
