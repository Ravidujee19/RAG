from __future__ import annotations

import csv
from typing import List, Optional

from app.models.document import Document


class CsvLoader:
    def __init__(self, text_column: Optional[str] = None) -> None:
        self._text_column = text_column

    def load(self, source: str) -> List[Document]:
        docs: List[Document] = []
        with open(source, "r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for index, row in enumerate(reader):
                if self._text_column and self._text_column in row:
                    text = row.get(self._text_column) or ""
                else:
                    text = " | ".join(str(value) for value in row.values() if value)
                docs.append(
                    Document(
                        id=f"{source}#row={index + 1}",
                        text=text,
                        metadata={"source": source, "row": index + 1},
                    )
                )
        return docs
