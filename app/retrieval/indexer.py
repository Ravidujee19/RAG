from __future__ import annotations

from typing import Iterable

from sentence_transformers import SentenceTransformer

from app.models.document import Document
from app.retrieval.vector_store import VectorStore


class Indexer:
    def __init__(self, vector_store: VectorStore, model_name: str) -> None:
        self._vector_store = vector_store
        self._model = SentenceTransformer(model_name)

    def index(self, documents: Iterable[Document]) -> int:
        docs = [doc for doc in documents if doc.text.strip()]
        if not docs:
            return 0
        texts = [doc.text for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        ids = [doc.id for doc in docs]
        embeddings = self._model.encode(texts, normalize_embeddings=True).tolist()
        self._vector_store.add_documents(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )
        return len(docs)
