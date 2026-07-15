import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "usage_summaries.db")

class LocalUsageDB:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    conversation_id TEXT,
                    summary_text TEXT NOT NULL,
                    tags TEXT,
                    model_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_summary(self, user_id: str, summary_text: str,
                    conversation_id: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    model_name: Optional[str] = None) -> int:
        tags_json = json.dumps(tags) if tags else None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO summaries (user_id, conversation_id, summary_text, tags, model_name)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, conversation_id, summary_text, tags_json, model_name)
            )
            conn.commit()
            return cursor.lastrowid

    def get_summaries(self, user_id: str, limit: int = 10,
                      offset: int = 0) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM summaries WHERE user_id = ?
                   ORDER BY created_at DESC LIMIT ? OFFSET ?""",
                (user_id, limit, offset)
            ).fetchall()
            return [dict(row) for row in rows]

    def search_summaries(self, user_id: str, keyword: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM summaries
                   WHERE user_id = ? AND summary_text LIKE ?""",
                (user_id, f"%{keyword}%")
            ).fetchall()
            return [dict(row) for row in rows]

    def delete_summary(self, summary_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM summaries WHERE id = ?", (summary_id,))
            conn.commit()
            return cursor.rowcount > 0