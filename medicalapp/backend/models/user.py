import sqlite3
import os

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

database_dir = os.path.join(
    current_dir,
    "..",
    "..",
    "database",
    "users.db"
)

database_dir = os.path.abspath(
    database_dir
)

connection = sqlite3.connect(
    database_dir,
    check_same_thread=False
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

phone TEXT UNIQUE,

birthday TEXT,

age INTEGER,

gender TEXT,

weight REAL,

height REAL

)
""")

connection.commit()