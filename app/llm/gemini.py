from __future__ import annotations

from typing import Any

from google import genai

from app.llm.base import LLMClient


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-3-flash-preview") -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        return response.text or ""
