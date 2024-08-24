import sqlite3
import os
from typing import Union, List, Optional

from prettytable import PrettyTable

from Utils.utils import calculate_age, get_zodiac_sign, user_modifiable_fields
from flaskr.models import User, UserIdentifiers, UserActivitiesModel


#Set up a UserDatabase class
class UserDatabase:
    def __init__(self, db_file='./Utils/users.db'):
        self.db_file = db_file

    def setup_database(self):
        #Sets up the user database by creating the necessary table.
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
            print(f"Deleted existing database file: {self.db_file}")

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        #list all attributes' types
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                birth_date TEXT,
                age INTEGER,
                gender TEXT,
                location TEXT,
                interests TEXT,
                smoking TEXT,
                drinking TEXT,
                zodiac_sign TEXT,
                mbti TEXT,
                profession TEXT,
                height INTEGER,
                bio TEXT,
                profile_pic TEXT
            )
        ''')

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id INTEGER PRIMARY KEY,
                        age TEXT,
                        gender TEXT,
                        location TEXT,
                        interests TEXT,
                        smoking TEXT,
                        drinking TEXT,
                        zodiac_sign TEXT,
                        mbti TEXT,
                        height INTEGER
                    )
                ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activities (
                user_id INTEGER PRIMARY KEY,
                liked_users TEXT,
                disliked_users TEXT,
                matches TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()
        conn.close()


    def insert_new_user(self, user: User) -> None:
        #Inserts a new user into the database.
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (name, birth_date, age, gender, location, interests, smoking, drinking, zodiac_sign, mbti, profession, height, bio, profile_pic)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.name, user.birth_date, calculate_age(user.birth_date), user.gender, user.location,
              ','.join(user.interests), user.smoking, user.drinking, get_zodiac_sign(user.birth_date), user.mbti,
              user.profession, user.height, user.bio, user.profile_pic))

        conn.commit()
        conn.close()

    def delete_account(self, user_id: int) -> None:
        #Deletes a user from the database.
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')
        all_users = cursor.fetchall()

        for user_data in all_users:
            (current_user_id, _, _, _, _, _, _, _, _, _, _, _, _, _) = user_data

            #First, remove the user's row from the user_activities table
            cursor.execute('DELETE FROM user_activities WHERE user_id = ?', (current_user_id,))

            #Next, update other users' liked_users, disliked_users, and matches lists to remove this user_id
            cursor.execute('SELECT user_id, liked_users, disliked_users, matches FROM user_activities')
            all_preferences = cursor.fetchall()

            for pref in all_preferences:
                current_user_id, liked_users, disliked_users, matches = pref

                #Convert comma-separated strings back to lists
                liked_users_list = list(map(int, liked_users.split(','))) if liked_users else []
                disliked_users_list = list(map(int, disliked_users.split(','))) if disliked_users else []
                matches_list = list(map(int, matches.split(','))) if matches else []

                #Remove the user_id from these lists if present
                if user_id in liked_users_list:
                    liked_users_list.remove(user_id)
                if user_id in disliked_users_list:
                    disliked_users_list.remove(user_id)
                if user_id in matches_list:
                    matches_list.remove(user_id)

                #Convert lists back to comma-separated strings
                liked_users = ','.join(map(str, liked_users_list))
                disliked_users = ','.join(map(str, disliked_users_list))
                matches = ','.join(map(str, matches_list))

                #Update the current user's preferences in the database
                cursor.execute('''
                    UPDATE user_activities
                    SET liked_users = ?, disliked_users = ?, matches = ?
                    WHERE user_id = ?
                ''', (liked_users, disliked_users, matches, current_user_id))

            #Commit the changes
            conn.commit()

        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    def update_account(self, user: UserIdentifiers) -> None:
        """Updates a user's information in the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        #Build the SQL query dynamically based on provided fields
        #Create the base query and the list to hold query parameters
        update_query = "UPDATE users SET "
        update_params = []

        #Dynamically build the query based on modifiable fields
        for field in user_modifiable_fields:
            value = getattr(user, field)
            if field == 'interests':
                #Convert list to a comma-separated string for interests
                value = ','.join(value)
            update_query += f"{field} = ?, "
            update_params.append(value)

        #Remove the trailing comma and space
        update_query = update_query.rstrip(', ')

        #Add the WHERE clause to update the correct user
        update_query += " WHERE user_id = ?"
        update_params.append(user.user_id)

        #Execute the update query
        cursor.execute(update_query, update_params)

        conn.commit()
        conn.close()

    def fetch_user(self, user_id: int) -> Union[User, None]:
        #Fetches a user's information from the database.
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            (user_id, name, birth_date, age, gender, location, interests, smoking, drinking, zodiac_sign, mbti,
             profession, height, bio, profile_pic) = user_data

            interests = interests.split(',')

            return User(
                user_id=user_id,
                name=name,
                birth_date=birth_date,
                age=age,
                gender=gender,
                location=location,
                interests=interests,
                smoking=smoking,
                drinking=drinking,
                zodiac_sign=zodiac_sign,
                mbti=mbti,
                profession=profession,
                height=height,
                bio=bio,
                profile_pic=profile_pic
            )

        return None


    def get_last_user_id(self):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # Execute the query to get the maximum user_id
            cursor.execute('SELECT MAX(user_id) FROM users')
            max_user_id = cursor.fetchone()[0]

            # Close the database connection
            conn.close()

            # Return the result, default to 0 if no users
            return max_user_id if max_user_id is not None else 0

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def fetch_all_users(self) -> List[User]:
        #Fetches all users from the database.
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')
        all_users = cursor.fetchall()

        conn.close()
        return all_users

    def display_users(self) -> None:
        #Displays all existing users in a tabular form.
        all_users = self.fetch_all_users()
        if all_users:
            table = PrettyTable()
            table.field_names = [
                "User ID", "Name", "Birth Date", "Age", "Gender", "Location", "Interests",
                "Smoking", "Drinking", "Zodiac Sign", "MBTI", "Profession", "Height",
                "Bio", "Profile Pic"
            ]

            for user_data in all_users:
                table.add_row(user_data)

            print(table)
        else:
            print("No users found in the database.")

    def fetch_user_activities(self, user_id: int) -> UserActivitiesModel:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT liked_users, disliked_users, matches FROM user_activities WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            liked_users_str, disliked_users_str, matches_str = row
            liked_users = list(map(int, liked_users_str.split(','))) if liked_users_str else []
            disliked_users = list(map(int, disliked_users_str.split(','))) if disliked_users_str else []
            matches = list(map(int, matches_str.split(','))) if matches_str else []

            return UserActivitiesModel(
                user_id=user_id,
                liked_users=liked_users,
                disliked_users=disliked_users,
                matches=matches
            )

        return UserActivitiesModel(user_id=user_id, liked_users=[], disliked_users=[], matches=[])

    def add_liked_users(self, current_user_id: int, user_to_like_user_id: int) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Fetch current user's activities
        cursor.execute('SELECT liked_users FROM user_activities WHERE user_id = ?', (current_user_id,))
        row = cursor.fetchone()
        if row:
            liked_users_str = row[0]
            liked_users = list(map(int, liked_users_str.split(','))) if liked_users_str else []
        else:
            liked_users = []

        if user_to_like_user_id not in liked_users:
            liked_users.append(user_to_like_user_id)
            liked_users_str = ','.join(map(str, liked_users))

            # Update current user's liked users
            cursor.execute('''
                UPDATE user_activities
                SET liked_users = ?
                WHERE user_id = ?
            ''', (liked_users_str, current_user_id))

            # Check if the liked user also likes the current user
            cursor.execute('SELECT liked_users FROM user_activities WHERE user_id = ?', (user_to_like_user_id,))
            row = cursor.fetchone()
            if row:
                liked_users_str = row[0]
                liked_users = list(map(int, liked_users_str.split(','))) if liked_users_str else []

                if current_user_id in liked_users:
                    # Update matches for both users
                    cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (current_user_id,))
                    row = cursor.fetchone()
                    if row:
                        matches_str = row[0]
                        matches = list(map(int, matches_str.split(','))) if matches_str else []
                        if user_to_like_user_id not in matches:
                            matches.append(user_to_like_user_id)
                            matches_str = ','.join(map(str, matches))
                            cursor.execute('''
                                UPDATE user_activities
                                SET matches = ?
                                WHERE user_id = ?
                            ''', (matches_str, current_user_id))

                    cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (user_to_like_user_id,))
                    row = cursor.fetchone()
                    if row:
                        matches_str = row[0]
                        matches = list(map(int, matches_str.split(','))) if matches_str else []
                        if current_user_id not in matches:
                            matches.append(current_user_id)
                            matches_str = ','.join(map(str, matches))
                            cursor.execute('''
                                UPDATE user_activities
                                SET matches = ?
                                WHERE user_id = ?
                            ''', (matches_str, user_to_like_user_id))

            conn.commit()
        conn.close()

    def add_disliked_users(self, current_user_id: int, user_to_dislike_user_id: int) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Fetch current user's disliked users
        cursor.execute('SELECT disliked_users FROM user_activities WHERE user_id = ?', (current_user_id,))
        row = cursor.fetchone()
        if row:
            disliked_users_str = row[0]
            disliked_users = list(map(int, disliked_users_str.split(','))) if disliked_users_str else []
        else:
            disliked_users = []

        if user_to_dislike_user_id not in disliked_users:
            disliked_users.append(user_to_dislike_user_id)
            disliked_users_str = ','.join(map(str, disliked_users))

            # Update current user's disliked users
            cursor.execute('''
                UPDATE user_activities
                SET disliked_users = ?
                WHERE user_id = ?
            ''', (disliked_users_str, current_user_id))

            conn.commit()
        conn.close()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Helper method to get a user by ID."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            (user_id, name, birth_date, age, gender, location, interests, smoking, drinking, zodiac_sign, mbti,
             profession, height, bio, profile_pic) = row
            interests_list = interests.split(',')

            return User(
                user_id=user_id,
                name=name,
                birth_date=birth_date,
                age=age,
                gender=gender,
                location=location,
                interests=interests_list,
                smoking=smoking,
                drinking=drinking,
                zodiac_sign=zodiac_sign,
                mbti=mbti,
                profession=profession,
                height=height,
                bio=bio,
                profile_pic=profile_pic
            )
        return None

    def fetch_matches(self, user_id: int) -> List[User]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Fetch the list of matches for the given user_id
        cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            matches_str = row[0]
            if matches_str:
                matches_ids = list(map(int, matches_str.split(',')))

                # Retrieve detailed information for each matched user
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute('SELECT user_id FROM users WHERE user_id IN (' + ','.join('?' * len(matches_ids)) + ')',
                               matches_ids)
                matched_user_ids = cursor.fetchall()
                conn.close()

                matched_users = []
                for (match_id,) in matched_user_ids:
                    user = self.get_user_by_id(match_id)
                    if user:
                        matched_users.append(user)

                return matched_users
        return []
