import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "activities.db"

def initialise_database():
    connection = sqlite3.connect(DB_PATH)
    connection.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs(
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity TEXT NOT NULL,
            duration INTEGER NOT NULL CHECK (duration > 0),
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
''')
    
    connection.commit()
    connection.close()

def insert_activity(activity, duration, notes):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute('''
            INSERT INTO activity_logs (activity, duration, notes)
            VALUES (?,?,?)
        ''', (activity, duration, notes))

        log_id = cursor.lastrowid
        connection.commit()

        return log_id

    finally:
        connection.close()

if __name__ == "__main__":
    initialise_database()
    print("Database initialised successfully!")