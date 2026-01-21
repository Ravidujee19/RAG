from __future__ import annotations

from typing import Protocol


class MemoryStore(Protocol):
    def add(self, text: str) -> None:
        ...

    def list(self, limit: int) -> list[str]:
        ...

    def clear(self) -> None:
        ...
