from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from sentence_transformers import SentenceTransformer

from app.retrieval.vector_store import RetrievedDocument, VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore, model_name: str) -> None:
        self._vector_store = vector_store
        self._model = SentenceTransformer(model_name)

    def retrieve(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        embedding = self._model.encode([query], normalize_embeddings=True)[0].tolist()
        results = self._vector_store.query(embedding, top_k=top_k)
        return [asdict(doc) for doc in results]
