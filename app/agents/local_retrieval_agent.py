from __future__ import annotations

from typing import Any, Dict

from app.agents.base import AgentResult
from app.retrieval.retriever import Retriever


class LocalRetrievalAgent:
    name = "retrieve_local"

    def __init__(self, retriever: Retriever) -> None:
        self._retriever = retriever

    def run(self, query: str, context: Dict[str, Any]) -> AgentResult:
        docs = self._retriever.retrieve(query, top_k=5)
        return AgentResult(
            name=self.name,
            content=f"retrieved {len(docs)} local documents",
            metadata={"type": "retrieval", "documents": docs},
        )
