# session_manager.py

import os

# Path to the file where the active user ID is stored
SESSION_FILE = './storage/active_user.txt'


def active_user(user_id):
    """
    Stores the logged-in user's ID into the file.

    :param user_id: The ID of the logged-in user.
    """
    with open(SESSION_FILE, 'w') as file:
        print("Activated User: ", user_id)
        file.write(str(user_id))


def fetch_active_user():
    """
    Fetches the active user's ID from the file.

    :return: The ID of the active user, or None if no user ID is stored.
    """
    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, 'r') as file:
        user_id = file.read().strip()

    return user_id if user_id else None


def end_user_session():
    """
    Removes the user ID from the file to end the user's session.
    """
    with open(SESSION_FILE, 'w') as file:
        pass


def is_user_authenticated():
    """
    Checks if a user is authenticated by verifying if there is an active user ID in the file.

    :return: True if a user is authenticated, False otherwise.
    """
    return fetch_active_user() is not None
