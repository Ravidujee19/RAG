from __future__ import annotations
from typing import Any, Dict
from app.agents.base import AgentResult


class WebSearchAgent:
    name = "search_web"

    def run(self, query: str, context: Dict[str, Any]) -> AgentResult:
        return AgentResult(
            name=self.name,
            content="web search is disabled in offline mode (This will be enabled in future versions)",
            metadata={"type": "tool", "tool": "web_search", "results": []},
        )
