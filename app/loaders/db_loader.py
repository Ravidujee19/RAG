from __future__ import annotations

import sqlite3
from typing import Iterable, List
from urllib.parse import urlparse

from app.models.document import Document


class SqliteLoader:
    def __init__(self, query: str, text_columns: Iterable[str]) -> None:
        self._query = query
        self._text_columns = list(text_columns)

    def load(self, source: str) -> List[Document]:
        db_path = self._resolve_path(source)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(self._query)
        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        conn.close()

        docs: List[Document] = []
        for index, row in enumerate(rows):
            record = dict(zip(columns, row))
            text = " | ".join(
                str(record.get(col, "")) for col in self._text_columns
            )
            docs.append(
                Document(
                    id=f"{source}#row={index + 1}",
                    text=text,
                    metadata={"source": source, "row": index + 1},
                )
            )
        return docs

    def _resolve_path(self, source: str) -> str:
        if source.startswith("sqlite://"):
            parsed = urlparse(source)
            if parsed.path:
                return parsed.path.lstrip("/")
        return source
