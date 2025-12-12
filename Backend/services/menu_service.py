import sqlite3
from Backend.utils.db_utils import get_db


class MenuService:

    @staticmethod
    def get_all_items():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, description FROM menu")
        items = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "name": r[1],
                "price": r[2],
                "description": r[3]
            }
            for r in items
        ]

    @staticmethod
    def search_items(keyword):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price, description FROM menu WHERE name LIKE ?",
            (f"%{keyword}%",),
        )
        items = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "name": r[1],
                "price": r[2],
                "description": r[3]
            }
            for r in items
        ]
