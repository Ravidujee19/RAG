from __future__ import annotations

from typing import Iterable, Optional, Sequence

from app.loaders.csv_loader import CsvLoader
from app.loaders.db_loader import SqliteLoader
from app.loaders.docx_loader import DocxLoader
from app.loaders.pdf_loader import PdfLoader
from app.loaders.text_loader import TextLoader
from app.models.document import Document
from app.retrieval.indexer import Indexer


class IngestionService:
    def __init__(self, indexer: Indexer) -> None:
        self._indexer = indexer

    def ingest_pdf(self, source: str) -> int:
        return self._indexer.index(PdfLoader().load(source))

    def ingest_docx(self, source: str) -> int:
        return self._indexer.index(DocxLoader().load(source))

    def ingest_text(self, source: str) -> int:
        return self._indexer.index(TextLoader().load(source))

    def ingest_csv(self, source: str, text_column: Optional[str] = None) -> int:
        return self._indexer.index(CsvLoader(text_column).load(source))

    def ingest_sqlite(
        self, source: str, query: str, text_columns: Iterable[str]
    ) -> int:
        loader = SqliteLoader(query=query, text_columns=text_columns)
        return self._indexer.index(loader.load(source))

    def reset_vector_store(self) -> None:
        if hasattr(self._indexer, "_vector_store"):
            vector_store = getattr(self._indexer, "_vector_store")
            if hasattr(vector_store, "reset"):
                vector_store.reset()
