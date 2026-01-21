from __future__ import annotations

from typing import List

from pypdf import PdfReader

from app.models.document import Document


class PdfLoader:
    def load(self, source: str) -> List[Document]:
        reader = PdfReader(source)
        docs: List[Document] = []
        for index, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            docs.append(
                Document(
                    id=f"{source}#page={index + 1}",
                    text=text,
                    metadata={"source": source, "page": index + 1},
                )
            )
        return docs
