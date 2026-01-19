from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol


@dataclass
class AgentResult:
    name: str
    content: str
    metadata: Dict[str, Any]


class BaseAgent(Protocol):
    name: str

    def run(self, query: str, context: Dict[str, Any]) -> AgentResult:
        ...
