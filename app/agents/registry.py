from __future__ import annotations

from typing import Dict, Iterable

from app.agents.base import BaseAgent


class AgentRegistry:
    def __init__(self, agents: Iterable[BaseAgent]) -> None:
        self._agents: Dict[str, BaseAgent] = {agent.name: agent for agent in agents}

    def get(self, name: str) -> BaseAgent:
        return self._agents[name]

    def list_names(self) -> list[str]:
        return sorted(self._agents.keys())
