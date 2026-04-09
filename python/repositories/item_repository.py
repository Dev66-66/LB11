import sqlite3
from typing import List, Optional, Tuple


class ItemRepository:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT
                )
            """)
            conn.commit()

    def get_all_items(self) -> List[Tuple]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT id, title, description FROM items")
            return cursor.fetchall()

    def get_item_by_id(self, item_id: int) -> Optional[Tuple]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, title, description FROM items WHERE id = ?",
                (item_id,)
            )
            return cursor.fetchone()

    def create_item(self, title: str, description: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO items (title, description) VALUES (?, ?)",
                (title, description)
            )
            conn.commit()
            return cursor.lastrowid

    def update_item(self, item_id: int, title: str, description: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "UPDATE items SET title = ?, description = ? WHERE id = ?",
                (title, description, item_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_item(self, item_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM items WHERE id = ?", (item_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
