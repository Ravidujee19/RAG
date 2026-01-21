from __future__ import annotations

from typing import List

from app.models.document import Document


class TextLoader:
    def load(self, source: str) -> List[Document]:
        with open(source, "r", encoding="utf-8") as handle:
            text = handle.read()
        return [
            Document(
                id=f"{source}#text",
                text=text,
                metadata={"source": source, "type": "text"},
            )
        ]
