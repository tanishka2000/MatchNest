import sqlite3


def init_db():
    conn = sqlite3.connect('./Utils/users.db')
    cursor = conn.cursor()

    # Create table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_cred (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create table for session tracking (or other needs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()


init_db()
