from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from app.agents.base import AgentResult


class ToolAgent:
    name = "tool"

    def run(self, query: str, context: Dict[str, Any]) -> AgentResult:
        if query.strip().lower() in {"time", "date", "now"}:
            now = datetime.utcnow().isoformat()
            return AgentResult(
                name=self.name,
                content=now,
                metadata={"type": "tool", "tool": "utc_time", "value": now},
            )

        message = context.get("message", "tool executed")
        return AgentResult(
            name=self.name,
            content=message,
            metadata={"type": "tool", "tool": "noop", "value": message},
        )
