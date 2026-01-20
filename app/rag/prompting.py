from __future__ import annotations

import json
from typing import Any, Dict, List


def planner_prompt(
    query: str,
    steps: List[Dict[str, Any]],
    available_agents: List[str],
) -> str:
    instructions = {
        "role": "planner",
        "task": "Select the next action for a multi-agent RAG system.",
        "constraints": [
            "Do not include chain-of-thought.",
            "Respond with a single JSON object.",
            "Valid actions: " + ", ".join(available_agents) + ", final",
            "Use action_input for any query to the selected agent.",
        ],
    }
    payload = {
        "instructions": instructions,
        "user_query": query,
        "previous_steps": steps,
    }
    return json.dumps(payload)


def rag_prompt(query: str, context: str, memories: List[str]) -> str:
    memory_block = "\n".join(memories)
    return (
        "You are a helpful assistant.\n"
        "Use the provided context to answer the question.\n"
        "If the context is insufficient, say so briefly.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{context}\n\n"
        f"Memory:\n{memory_block}\n"
    )
