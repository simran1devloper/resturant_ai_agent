import sqlite3
from Backend.utils.db_utils import get_db


class OrderService:

    @staticmethod
    def create_order(item_id, quantity):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (item_id, quantity, status) VALUES (?, ?, 'pending')",
            (item_id, quantity),
        )
        conn.commit()
        order_id = cursor.lastrowid
        conn.close()
        return {"order_id": order_id, "status": "pending"}

    @staticmethod
    def get_order(order_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, item_id, quantity, status FROM orders WHERE id = ?",
            (order_id,),
        )
        order = cursor.fetchone()
        conn.close()

        if not order:
            return None

        return {
            "order_id": order[0],
            "item_id": order[1],
            "quantity": order[2],
            "status": order[3],
        }

    @staticmethod
    def confirm_order(order_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = 'confirmed' WHERE id = ?",
            (order_id,),
        )
        conn.commit()
        conn.close()
        return {"order_id": order_id, "status": "confirmed"}
