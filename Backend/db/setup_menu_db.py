import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "menu.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
MENU_JSON = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Rag",
    "menu.json"
)


def setup_database():
    """Create database, load schema, and insert menu items from JSON."""
    # Connect DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load schema
    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Load menu data
    if not os.path.exists(MENU_JSON):
        print("menu.json not found!")
        return

    with open(MENU_JSON, "r") as f:
        menu_data = json.load(f)

    # Insert items
    for item in menu_data:
        cursor.execute(
            "INSERT INTO menu (name, price, description) VALUES (?, ?, ?)",
            (item["name"], item["price"], item.get("description", ""))
        )

    conn.commit()
    conn.close()

    print("Database setup complete → menu.db loaded successfully.")


if __name__ == "__main__":
    setup_database()
