from __future__ import annotations

import hashlib
import sqlite3
from typing import Optional


class LLMCache:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_cache (
                prompt_hash TEXT PRIMARY KEY,
                response_text TEXT NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()

    def get(self, prompt: str) -> Optional[str]:
        prompt_hash = self._hash(prompt)
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT response_text FROM llm_cache WHERE prompt_hash = ?",
            (prompt_hash,),
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0]
        return None

    def set(self, prompt: str, response: str) -> None:
        prompt_hash = self._hash(prompt)
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO llm_cache (prompt_hash, response_text) VALUES (?, ?)",
            (prompt_hash, response),
        )
        conn.commit()
        conn.close()

    def clear(self) -> None:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM llm_cache")
        conn.commit()
        conn.close()

    def _hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()
