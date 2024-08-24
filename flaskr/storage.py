# create tables
"""
1. UserDB
2. UserCred
3. UserActivity
"""
import os
import sqlite3

def init_user_cred(user_cred_db_file):
    # Sets up the user database by creating the necessary table.
    # if os.path.exists(user_cred_db_file):
    #     os.remove(user_cred_db_file)
    #     print(f"Deleted existing database file: {user_cred_db_file}")

    conn = sqlite3.connect(user_cred_db_file)
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

    conn.commit()
    conn.close()
