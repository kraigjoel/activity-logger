import sqlite3
from pathlib import Path

DB_PATH = Path("/activities.db")

def initialise_database():
    connection = sqlite3.connect('DB_PATH')

    connection.close()

print(__name__)