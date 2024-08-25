import sqlite3
from typing import Union

from flaskr.models import UserActivitiesModel


class UserActivities:
    def __init__(self, db_file):
        self.db_file = db_file

    def _ensure_user_exists(self, user_id):
        """Ensure that a user activity record exists. If not, create it with default values."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM user_activities WHERE user_id = ?', (user_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO user_activities (user_id, liked_users, disliked_users, matches)
                VALUES (?, '', '', '')
            ''', (user_id,))

        conn.commit()
        conn.close()

    def add_liked_user(self, current_user_id, user_to_like_user_id):
        """Add the user to the liked_users list if not already present."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Ensure both users exist in the database
        self._ensure_user_exists(current_user_id)
        self._ensure_user_exists(user_to_like_user_id)

        # fetch current user's activities
        current_user_activities = self.fetch_user_activity(current_user_id)
        current_user_liked_list = list(
            map(int, current_user_activities.liked_users.split(','))) if current_user_activities.liked_users else []

        # if user_to_like is not in current user's like list, then add them to liked list
        if user_to_like_user_id not in current_user_liked_list:
            current_user_liked_list.append(user_to_like_user_id)
            current_user_liked_str = ','.join(map(str, current_user_liked_list))
            current_user_matches_str = current_user_activities.matches

            # fetch user_to_like activities
            user_to_like_activities = self.fetch_user_activity(user_to_like_user_id)
            user_to_like_liked_list = list(
                map(int, user_to_like_activities.liked_users.split(','))) if user_to_like_activities.liked_users else []

            # now check it's like list
            if current_user_id in user_to_like_liked_list:
                user_to_like_matches_list = list(
                    map(int, user_to_like_activities.matches.split(','))) if user_to_like_activities.matches else []
                current_user_matches_list = list(
                    map(int, current_user_activities.matches.split(','))) if current_user_activities.matches else []
                user_to_like_matches_list.append(current_user_id)
                current_user_matches_list.append(user_to_like_user_id)

                user_to_like_matches_str = ','.join(map(str, user_to_like_matches_list))
                current_user_matches_str = ','.join(map(str, current_user_matches_list))

                # update matches for user_to_like
                cursor.execute('''
                    UPDATE user_activities
                    SET matches = ?
                    WHERE user_id = ?
                ''', (user_to_like_matches_str, user_to_like_user_id))

            # update matches for current_user
            cursor.execute('''
                UPDATE user_activities
                SET liked_users = ?, matches = ?
                WHERE user_id = ?
            ''', (current_user_liked_str, current_user_matches_str, current_user_id))

            conn.commit()
        conn.close()

    def add_disliked_user(self, current_user_id, user_to_dislike_user_id):
        """Append a user ID to the disliked_users list."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Ensure both users exist in the database
        self._ensure_user_exists(current_user_id)
        self._ensure_user_exists(user_to_dislike_user_id)

        # fetch current user's activities
        current_user_activities = self.fetch_user_activity(current_user_id)
        current_user_disliked_list = list(map(int, current_user_activities.disliked_users.split(
            ','))) if current_user_activities.disliked_users else []

        # if user_to_dislike is not in current user's dislike list, then add them to disliked list
        if user_to_dislike_user_id not in current_user_disliked_list:
            current_user_disliked_list.append(user_to_dislike_user_id)
            current_user_disliked_str = ','.join(map(str, current_user_disliked_list))

            # update disliked_users for current_user
            cursor.execute('''
                UPDATE user_activities
                SET disliked_users = ?
                WHERE user_id = ?
            ''', (current_user_disliked_str, current_user_id))

            conn.commit()
        conn.close()

    def view_matches(self, user_id):
        """View the match list for a user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT matches FROM user_activities WHERE user_id = ?', (user_id,))
        matches = cursor.fetchone()

        conn.close()

        if matches:
            return list(map(int, matches[0].split(','))) if matches[0] else []
        else:
            return []

    def fetch_user_activity(self, user_id) -> Union[UserActivitiesModel, None]:
        """Loads the user activities from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT liked_users, disliked_users, matches FROM user_activities WHERE user_id = ?',
                       (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            liked_users_str, disliked_users_str, matches_str = result

            return UserActivitiesModel(
                user_id=user_id,
                liked_users=liked_users_str,
                disliked_users=disliked_users_str,
                matches=matches_str
            )

        return None
