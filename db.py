import sqlite3
from .config import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS infts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    owner TEXT,
    tag TEXT,
    cid TEXT,
    traits_json TEXT,
    score REAL DEFAULT 0,
    created_at TEXT
)
""")

conn.commit()