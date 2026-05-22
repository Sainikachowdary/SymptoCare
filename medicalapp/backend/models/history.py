import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

database_dir = os.path.join(
    current_dir,
    "..",
    "..",
    "database",
    "history.db"
)

database_dir = os.path.abspath(database_dir)

connection = sqlite3.connect(
    database_dir,
    check_same_thread=False
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symptoms TEXT,
    prediction TEXT,
    confidence REAL,
    date TEXT
)
""")

connection.commit()