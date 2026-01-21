from __future__ import annotations

from app.memory.long_term import LongTermMemory
from app.memory.short_term import ShortTermMemory


class MemoryManager:
    def __init__(self, short_term: ShortTermMemory, long_term: LongTermMemory) -> None:
        self._short = short_term
        self._long = long_term

    def remember(self, text: str) -> None:
        self._short.add(text)
        self._long.add(text)

    def recall(self, limit: int = 10) -> list[str]:
        return self._short.list(limit)

    def clear(self) -> None:
        self._short.clear()
        self._long.clear()
