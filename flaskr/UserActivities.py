import sqlite3
from flaskr.models import User, UserActivitiesModel


class UserActivities:
    def __init__(self, user_activities: UserActivitiesModel, db_file: str):
        self.db_file = db_file
        self.user_id = user_activities.user_id
        self.liked_users = list(map(int, user_activities.liked_users.split(','))) if user_activities.liked_users else []
        self.disliked_users = list(
            map(int, user_activities.disliked_users.split(','))) if user_activities.disliked_users else []
        self.matches = list(map(int, user_activities.matches.split(','))) if user_activities.matches else []

    def add_liked_user(self, user_to_like: UserActivitiesModel):
        """Add the user to the liked_users list if not already present."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if user_to_like.user_id not in self.liked_users:
            self.liked_users.append(user_to_like.user_id)
            liked_users_str = ','.join(map(str, self.liked_users))
            matches_str = ','.join(map(str, self.matches))

            cursor.execute('''
                UPDATE user_activities
                SET liked_users = ?, matches = ?
                WHERE user_id = ?
            ''', (liked_users_str, matches_str, self.user_id))
            print(f"Updated liked_users for {self.user_id}: {liked_users_str}")
            print(f"Updated matches for {self.user_id}: {matches_str}")

            if self.user_id in user_to_like.liked_users:
                print(f"Looks like a match with {self.user_id} and {user_to_like.user_id}")
                self.matches.append(user_to_like.user_id)
                matches_of_user_to_like = list(
                    map(int, user_to_like.matches.split(','))) if user_to_like.matches else []
                if self.user_id not in matches_of_user_to_like:
                    matches_of_user_to_like.append(self.user_id)
                matches_str_updated = ','.join(map(str, matches_of_user_to_like))

                cursor.execute('''
                    UPDATE user_activities
                    SET matches = ?
                    WHERE user_id = ?
                ''', (matches_str_updated, user_to_like.user_id))
                print(f"Updated matches for {user_to_like.user_id}: {matches_str_updated}")

        conn.commit()
        conn.close()

    def add_disliked_user(self, user_to_dislike: UserActivitiesModel):
        """Appends a user ID to the disliked_users list."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if user_to_dislike.user_id not in self.disliked_users:
            self.disliked_users.append(user_to_dislike.user_id)
            disliked_users_str = ','.join(map(str, self.disliked_users))

            cursor.execute('''
                UPDATE user_activities
                SET disliked_users = ?
                WHERE user_id = ?
            ''', (disliked_users_str, self.user_id))
            print(f"Updated disliked_users for {self.user_id}: {disliked_users_str}")

        conn.commit()
        conn.close()

    def view_matches(self):
        """View match list for a user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (self.user_id,))
        matches = cursor.fetchone()

        conn.close()

        if matches:
            return list(map(int, matches[0].split(',')))
        else:
            return []

    def load_from_db(self):
        """Loads the user preferences from the database."""
        conn = sqlite3.connect(self.db_file)
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
