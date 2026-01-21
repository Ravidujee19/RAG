from __future__ import annotations

import sqlite3
from typing import List

from app.memory.store import MemoryStore


class LongTermMemory(MemoryStore):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()

    def add(self, text: str) -> None:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO memory (text) VALUES (?)", (text,))
        conn.commit()
        conn.close()

    def list(self, limit: int) -> List[str]:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT text FROM memory ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = [row[0] for row in cur.fetchall()]
        conn.close()
        return rows

    def clear(self) -> None:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM memory")
        conn.commit()
        conn.close()
