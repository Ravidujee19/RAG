from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from app.agents.registry import AgentRegistry

from app.llm.base import LLMClient
from app.rag.pipeline import RAGPipeline
from app.rag.prompting import planner_prompt


@dataclass
class OrchestrationResult:
    answer: str
    steps: List[Dict[str, Any]]


class AggregatorAgent:
    name = "aggregator"

    def __init__(
        self,
        llm: LLMClient,
        registry: AgentRegistry,
        rag: RAGPipeline,
        max_steps: int = 4,
    ) -> None:
        self._llm = llm
        self._registry = registry
        self._rag = rag
        self._max_steps = max_steps

    def run(self, query: str, context: Dict[str, Any]) -> OrchestrationResult:
        steps: List[Dict[str, Any]] = []
        retrieved: List[Dict[str, Any]] = []
        tool_outputs: List[Dict[str, Any]] = []
        memories: List[str] = context.get("memories", [])

        for _ in range(self._max_steps):
            prompt = planner_prompt(query, steps, self._registry.list_names())
            raw = self._llm.generate(prompt)
            parsed = self._parse_planner_json(raw)

            action = parsed.get("action", "")
            action_input = parsed.get("action_input", "")

            if action == "final":
                answer = self._rag.generate(query, retrieved, memories, tool_outputs)
                return OrchestrationResult(answer=answer, steps=steps)

            result = self._dispatch(action, action_input, context)
            step = {
                "action": action,
                "input": action_input,
                "output": result.content,
                "metadata": result.metadata,
            }
            steps.append(step)

            if result.metadata.get("type") == "retrieval":
                retrieved.extend(result.metadata.get("documents", []))
            if result.metadata.get("type") == "tool":
                tool_outputs.append(result.metadata)

        answer = self._rag.generate(query, retrieved, memories, tool_outputs)
        return OrchestrationResult(answer=answer, steps=steps)

    def _dispatch(self, action: str, action_input: str, context: Dict[str, Any]):
        if action not in self._registry.list_names():
            return self._registry.get("tool").run(
                query=action_input or action,
                context={"message": f"Unknown action: {action}"},
            )
        return self._registry.get(action).run(query=action_input, context=context)

    def _parse_planner_json(self, raw: str) -> Dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"action": "final", "action_input": "", "final": raw}
