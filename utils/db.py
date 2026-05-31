import sqlite3

conn = sqlite3.connect(
    "patients.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    systolic INTEGER,
    diastolic INTEGER,
    cholesterol INTEGER,
    glucose INTEGER,
    prediction TEXT,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()