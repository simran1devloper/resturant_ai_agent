import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "db",
    "menu.db"
)


def get_db():
    """Return a SQLite3 connection to the menu database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
