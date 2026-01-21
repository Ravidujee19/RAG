from __future__ import annotations

from typing import Protocol, Sequence

from app.models.document import Document


class BaseLoader(Protocol):
    def load(self, source: str) -> Sequence[Document]:
        ...
