import sqlite3


# CREATE CONNECTION
conn = sqlite3.connect(
    "edugenie.db",
    check_same_thread=False
)

cursor = conn.cursor()


# CREATE USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT
)
""")

conn.commit()

# CREATE CHAT HISTORY TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    question TEXT,

    answer TEXT
)
""")

conn.commit()

# REGISTER USER
def register_user(username, password):

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()


# LOGIN USER
def login_user(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    return cursor.fetchone()

# SAVE CHAT
def save_chat(username, question, answer):

    cursor.execute(
        """
        INSERT INTO chat_history
        (username, question, answer)

        VALUES (?, ?, ?)
        """,
        (username, question, answer)
    )

    conn.commit()

# GET CHAT HISTORY
def get_chat_history(username):

    cursor.execute(
        """
        SELECT question, answer
        FROM chat_history
        WHERE username=?
        """,
        (username,)
    )

    return cursor.fetchall()