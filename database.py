import sqlite3
import os

def get_conn():
    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Ensure database file exists
    db_path = "data/quiz.db"
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        otp TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        duration INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        question TEXT,
        opt1 TEXT, opt2 TEXT, opt3 TEXT, opt4 TEXT,
        answer TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quiz_id INTEGER,
        score INTEGER,
        date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quiz_id INTEGER,
        started INTEGER,
        finished INTEGER
    )
    """)

    conn.commit()
    conn.close()
