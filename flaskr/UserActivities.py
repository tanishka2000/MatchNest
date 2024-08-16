import sqlite3

from prettytable import PrettyTable

from flaskr.models import User


class UserActivities:
    def __init__(self, user_id, liked_users=None, disliked_users=None, matches=None):
        self.user_id = user_id
        self.liked_users = liked_users if liked_users is not None else []
        self.disliked_users = disliked_users if disliked_users is not None else []
        self.matches = matches if matches is not None else []

    def add_liked_user(self, user_to_like: User):
        # Add the user to the liked_users list if not already present
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        if user_to_like.user_id not in self.liked_users:
            self.liked_users.append(user_to_like)

        if self.user_id in user_to_like.liked_users:
            self.matches.append(user_to_like.user_id)
            matches_of_user_to_like = list(map(int, user_to_like.matches.split(','))) if user_to_like.matches else []

            matches_str_updated = ','.join(map(str, matches_of_user_to_like))

            cursor.execute('''
                                    UPDATE user_activities
                                    SET matches = ?
                                    WHERE user_id = ?
                                ''', (matches_str_updated, user_to_like.user_id))

        # Update the database with the new liked_users and matches lists
        liked_users_str = ','.join(map(str, self.liked_users))
        matches_str = ','.join(map(str, self.matches))

        cursor.execute('''
            UPDATE user_activities
            SET liked_users = ?, matches = ?
            WHERE user_id = ?
        ''', (liked_users_str, matches_str, self.user_id))

        conn.commit()
        conn.close()

    def add_disliked_user(self, user_to_dislike: User):
        """Appends a user ID to the disliked_users list."""
        if user_to_dislike.user_id not in self.disliked_users:
            self.disliked_users.append(user_to_dislike.user_id)

            disliked_users_str = ','.join(map(str, self.disliked_users))
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                                                UPDATE user_activities
                                                SET matches = ?
                                                WHERE user_id = ?
                                            ''', (disliked_users_str, user_to_dislike.user_id))
            conn.commit()
            conn.close()

    def view_matches(self, db_file):
        """View match list for a user."""
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (self.user_id,))
        matches = cursor.fetchall()

        conn.close()

        if matches:
            table = PrettyTable()
            table.field_names = [
                "User ID", "matches"
            ]

            for user_data in matches:
                table.add_row((self.user_id, matches))

            print(table)
            return self.matches
        else:
            print("No matches found in the database.")
            return None

    def save_to_db(self, db_file):
        """Saves the user preferences to the database."""
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activities (
                user_id INTEGER PRIMARY KEY,
                liked_users TEXT,
                disliked_users TEXT,
                matches TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Convert lists to comma-separated strings for storage
        liked_users_str = ','.join(map(str, self.liked_users))
        disliked_users_str = ','.join(map(str, self.disliked_users))
        matches_str = ','.join(map(str, self.matches))

        cursor.execute('''
            INSERT OR REPLACE INTO user_activities (user_id, liked_users, disliked_users, matches)
            VALUES (?, ?, ?, ?)
        ''', (self.user_id, liked_users_str, disliked_users_str, matches_str))

        conn.commit()
        conn.close()

    def load_from_db(self, db_file):
        """Loads the user preferences from the database."""
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT liked_users, disliked_users, matches FROM user_activities WHERE user_id = ?',
                       (self.user_id,))
        result = cursor.fetchone()

        if result:
            liked_users_str, disliked_users_str, matches_str = result
            self.liked_users = list(map(int, liked_users_str.split(','))) if liked_users_str else []
            self.disliked_users = list(map(int, disliked_users_str.split(','))) if disliked_users_str else []
            self.matches = list(map(int, matches_str.split(','))) if matches_str else []

        conn.close()

    def __repr__(self):
        return (f"UserActivities(user_id={self.user_id}, liked_users={self.liked_users}, "
                f"disliked_users={self.disliked_users}, matches={self.matches})")
