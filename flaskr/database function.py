import sqlite3
import os

def setup_database():

  db_file = 'users.db'
  # If DB exists - delete it upon setup:
  if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted existing database file: {db_file}")
  # Create a connection to the SQLite database

  conn = sqlite3.connect(db_file)

  # Create a cursor object
  cursor = conn.cursor()

  # Create a table for storing user information
  cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY,
          name TEXT,
          birth_date TEXT,
          gender TEXT,
          location TEXT,
          interests TEXT,
          smoking TEXT,
          drinking TEXT,
          constellation TEXT,
          mbti TEXT,
          profession TEXT,
          height INTEGER,
          bio TEXT,
          liked_users TEXT,
          disliked_users TEXT,
          matches TEXT
      )
  ''')

  # Commit changes and close the connection
  conn.commit()
  conn.close()

#%%
def insert_user(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Convert lists to comma-separated strings for storage
    liked_users = ','.join(map(str, user.liked_users))
    disliked_users = ','.join(map(str, user.disliked_users))
    matches = ','.join(map(str, user.matches))

    cursor.execute('''
        INSERT INTO users (user_id, name, birth_date, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user.user_id, user.name, user.birth_date, user.gender, user.location,
          ','.join(user.interests), user.smoking, user.drinking, user.constellation, user.mbti, user.profession, user.height, user.bio, liked_users, disliked_users, matches))

    conn.commit()
    conn.close()

#%%
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # First, update other users' liked_users, disliked_users, and matches lists to remove this user
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    for user_data in all_users:
        current_user_id, name, brith_date, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches = user_data

        liked_users_list = list(map(int, liked_users.split(','))) if liked_users else []
        disliked_users_list = list(map(int, disliked_users.split(','))) if disliked_users else []
        matches_list = list(map(int, matches.split(','))) if matches else []

        if user_id in liked_users_list:
            liked_users_list.remove(user_id)
        if user_id in disliked_users_list:
            disliked_users_list.remove(user_id)
        if user_id in matches_list:
            matches_list.remove(user_id)

        # Update the current user with the modified lists
        liked_users = ','.join(map(str, liked_users_list))
        disliked_users = ','.join(map(str, disliked_users_list))
        matches = ','.join(map(str, matches_list))

        cursor.execute('''
            UPDATE users
            SET liked_users = ?, disliked_users = ?, matches = ?
            WHERE user_id = ?
        ''', (liked_users, disliked_users, matches, current_user_id))

    # Now delete the user from the database
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))

    conn.commit()
    conn.close()

#%%
def update_user(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    liked_users = ','.join(map(str, user.liked_users))
    disliked_users = ','.join(map(str, user.disliked_users))
    matches = ','.join(map(str, user.matches))

    cursor.execute('''
        UPDATE users
        SET liked_users = ?, disliked_users = ?, matches = ?
        WHERE user_id = ?
    ''', (liked_users, disliked_users, matches, user.user_id))

    conn.commit()
    conn.close()

#%%
def fetch_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        user_id, name, brith_date, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches = user_data

        # Convert comma-separated strings back to lists
        interests = interests.split(',')
        liked_users = list(map(int, liked_users.split(','))) if liked_users else []
        disliked_users = list(map(int, disliked_users.split(','))) if disliked_users else []
        matches = list(map(int, matches.split(','))) if matches else []

        return User(user_id, name, brith_date, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches )
    else:
        return None  # User not found





