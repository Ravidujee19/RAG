from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMResponse:
    text: str
    raw: object | None = None


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...
