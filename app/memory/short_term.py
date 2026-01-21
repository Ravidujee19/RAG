from __future__ import annotations

from collections import deque

from app.memory.store import MemoryStore


class ShortTermMemory(MemoryStore):
    def __init__(self, max_items: int = 20) -> None:
        self._buffer = deque(maxlen=max_items)

    def add(self, text: str) -> None:
        self._buffer.append(text)

    def list(self, limit: int) -> list[str]:
        return list(self._buffer)[-limit:]

    def clear(self) -> None:
        self._buffer.clear()
