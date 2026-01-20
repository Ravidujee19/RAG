from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import chromadb


@dataclass
class RetrievedDocument:
    id: str
    text: str
    metadata: Dict[str, Any]


class VectorStore:
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str] | None = None,
        embeddings: List[List[float]] | None = None,
    ) -> None:
        raise NotImplementedError

    def query(self, query_embedding: List[float], top_k: int) -> List[RetrievedDocument]:
        raise NotImplementedError


class ChromaVectorStore(VectorStore):
    def __init__(self, path: str, collection: str) -> None:
        self._client = chromadb.PersistentClient(path=path)
        self._collection = self._client.get_or_create_collection(name=collection)
        self._collection_name = collection

    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str] | None = None,
        embeddings: List[List[float]] | None = None,
    ) -> None:
        ids = ids or [f"doc-{i}" for i in range(len(texts))]
        self._collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )

    def query(self, query_embedding: List[float], top_k: int) -> List[RetrievedDocument]:
        result = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        docs = []
        for idx, text in zip(result["ids"][0], result["documents"][0]):
            docs.append(RetrievedDocument(id=str(idx), text=text, metadata={}))
        return docs

    def reset(self) -> None:
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(name=self._collection_name)
