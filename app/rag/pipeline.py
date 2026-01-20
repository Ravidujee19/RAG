from __future__ import annotations

from typing import Any, Dict, List

from app.llm.base import LLMClient
from app.rag.prompting import rag_prompt


class RAGPipeline:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def generate(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        memories: List[str],
        tools: List[Dict[str, Any]],
    ) -> str:
        context_parts = []
        for doc in documents:
            text = doc.get("text", "")
            if text:
                context_parts.append(text)

        for tool in tools:
            value = tool.get("value", "")
            if value:
                context_parts.append(f"[tool:{tool.get('tool')}] {value}")

        context = "\n".join(context_parts)
        prompt = rag_prompt(query, context, memories)
        return self._llm.generate(prompt)
