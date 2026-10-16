import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "activities.db"

def initialise_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT NOT NULL,
                duration INTEGER NOT NULL CHECK (duration > 0),
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
""")

def insert_activity(activity, duration, notes):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute("""
            INSERT INTO activity_logs (activity, duration, notes)
            VALUES (?, ?, ?)
        """, (activity, duration, notes))

        return cursor.lastrowid


if __name__ == "__main__":
    initialise_database()
    print("Database initialized successfully!")