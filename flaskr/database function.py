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
          age INTEGER,
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


from datetime import datetime


# dob have to be in YYYY-MM-DD
def calculate_age(dob):
    dob = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


def get_zodia_sign(dob):
    dob = datetime.strptime(dob, "%Y-%m-%d")
    zodiac_signs = [
        ("Capricorn", (datetime(dob.year, 12, 22), datetime(dob.year, 1, 19))),
        ("Aquarius", (datetime(dob.year, 1, 20), datetime(dob.year, 2, 18))),
        ("Pisces", (datetime(dob.year, 2, 19), datetime(dob.year, 3, 20))),
        ("Aries", (datetime(dob.year, 3, 21), datetime(dob.year, 4, 19))),
        ("Taurus", (datetime(dob.year, 4, 20), datetime(dob.year, 5, 20))),
        ("Gemini", (datetime(dob.year, 5, 21), datetime(dob.year, 6, 20))),
        ("Cancer", (datetime(dob.year, 6, 21), datetime(dob.year, 7, 22))),
        ("Leo", (datetime(dob.year, 7, 23), datetime(dob.year, 8, 22))),
        ("Virgo", (datetime(dob.year, 8, 23), datetime(dob.year, 9, 22))),
        ("Libra", (datetime(dob.year, 9, 23), datetime(dob.year, 10, 22))),
        ("Scorpio", (datetime(dob.year, 10, 23), datetime(dob.year, 11, 21))),
        ("Sagittarius", (datetime(dob.year, 11, 22), datetime(dob.year, 12, 21))),
    ]

    for sign, (start, end) in zodiac_signs():
        if start <= dob <= end:
            return sign

    if dob.month == 1 and dob.day <= 19:
        return "Capricorn"


# %%
def insert_user(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Convert lists to comma-separated strings for storage
    liked_users = ','.join(map(str, user.liked_users))
    disliked_users = ','.join(map(str, user.disliked_users))
    matches = ','.join(map(str, user.matches))

    cursor.execute('''
        INSERT INTO users (user_id, name, birth_date, age, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user.user_id, user.name, user.birth_date, calculate_age(user.birth_date), user.gender, user.location,
          ','.join(user.interests), user.smoking, user.drinking, get_zodia_sign(user.birth_date), user.mbti,
          user.profession, user.height, user.bio, liked_users, disliked_users, matches))

    conn.commit()
    conn.close()


# %%
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # First, update other users' liked_users, disliked_users, and matches lists to remove this user
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    for user_data in all_users:
        current_user_id, name, brith_date, age, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches = user_data

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


# %%
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


# %%
def fetch_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        user_id, name, brith_date, age, gender, location, interests, smoking, drinking, constellation, mbti, profession, height, bio, liked_users, disliked_users, matches = user_data

        # Convert comma-separated strings back to lists
        interests = interests.split(',')
        liked_users = list(map(int, liked_users.split(','))) if liked_users else []
        disliked_users = list(map(int, disliked_users.split(','))) if disliked_users else []
        matches = list(map(int, matches.split(','))) if matches else []

        return User(user_id, name, brith_date, gender, location, interests, smoking, drinking, constellation, mbti,
                    profession, height, bio, liked_users, disliked_users, matches)
    else:
        return None  # User not found





