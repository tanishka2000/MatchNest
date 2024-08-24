import numpy as np
import pandas as pd

from flaskr.UserActivities import UserActivities
from flaskr.UserDatabase import UserDatabase
from Utils.constants import MBTI_PAIRS, ZODIAC_COMPATIBILITY
from flaskr.models import User

db = UserDatabase()

# Load All Users into a Pandas DataFrame
data = db.fetch_all_users()
# Define the column names based on the order of the tuple elements
columns = [
    'user_id', 'name', 'birth_date', 'age', 'gender', 'location',
    'interests', 'smoking', 'drinking', 'zodiac_sign', 'mbti',
    'profession', 'height', 'bio', 'profile_pic'
]

# Convert the list of tuples to a DataFrame
df = pd.DataFrame(data, columns=columns)
print(df.head())
df['interests'] = df['interests'].apply(lambda x: x.split(',') if x else [])


# Define MBTI compatibility score
def get_mbti_score(mbti1, mbti2):
    preferred_matches = MBTI_PAIRS.get(mbti1, [])
    return 1.0 if mbti2 in preferred_matches else 0.0


# Define the zodiac compatibility score
def get_zodiac_compatibility(zodiac1, zodiac2):
    # Ensure the score is for both directions
    return ZODIAC_COMPATIBILITY.get((zodiac1, zodiac2),
                                    ZODIAC_COMPATIBILITY.get((zodiac2, zodiac1), 0.0))


# Define smoking and drinking compatibility scores
def get_smoking_score(smoking1, smoking2):
    return 1.0 if smoking1 == smoking2 else 0.0


def get_drinking_score(drinking1, drinking2):
    return 1.0 if drinking1 == drinking2 else 0.0


# Compute Compatibility Scores
def compute_compatibility_scores(logged_in_user, users_df):
    # Exclude the logged-in user from potential matches
    potential_matches = users_df[users_df['user_id'] != logged_in_user.user_id].copy()

    # Calculate location compatibility score
    potential_matches['location_score'] = (potential_matches['location'] == logged_in_user.location).astype(float)

    # Calculate age difference score
    potential_matches['age_diff_score'] = 1 / (1 + np.abs(potential_matches['age'] - logged_in_user.age))

    # Calculate zodiac compatibility score
    potential_matches['zodiac_score'] = potential_matches.apply(
        lambda row: get_zodiac_compatibility(
            logged_in_user.zodiac_sign, logged_in_user.zodiac_sign,
        ), axis=1
    )

    # Calculate MBTI compatibility score
    potential_matches['mbti_score'] = potential_matches.apply(
        lambda row: get_mbti_score(
            logged_in_user.mbti, row['mbti']
        ), axis=1
    )

    # Calculate smoking compatibility score
    potential_matches['smoking_score'] = potential_matches.apply(
        lambda row: get_smoking_score(
            logged_in_user.smoking, row['smoking']
        ), axis=1
    )

    # Calculate drinking compatibility score
    potential_matches['drinking_score'] = potential_matches.apply(
        lambda row: get_drinking_score(
            logged_in_user.drinking, row['drinking']
        ), axis=1
    )

    # Convert interests lists into a set for the logged-in user for faster comparison
    logged_in_interests_set = set(logged_in_user.interests)

    # Optimize shared interests score calculation
    def calculate_jaccard_similarity_vectorized(interests):
        interests_set = set(interests)
        intersection_size = len(logged_in_interests_set & interests_set)
        union_size = len(logged_in_interests_set | interests_set)
        return intersection_size / union_size if union_size > 0 else 0

    # Apply the vectorized Jaccard similarity calculation to all potential matches
    potential_matches['interests_score'] = potential_matches['interests'].apply(calculate_jaccard_similarity_vectorized)

    # Combine the individual scores into a final compatibility score
    potential_matches['compatibility_score'] = (
            0.25 * potential_matches['location_score'] +  # Adjusted weight for location score
            0.2 * potential_matches['age_diff_score'] +  # Adjusted weight for age score
            0.15 * potential_matches['zodiac_score'] +  # Zodiac score with its weight
            0.1 * potential_matches['mbti_score'] +  # MBTI score with its weight
            0.1 * potential_matches['smoking_score'] +  # Smoking score with its weight
            0.1 * potential_matches['drinking_score'] +  # Drinking score with its weight
            0.1 * potential_matches['interests_score']  # Interests score remains the same
    )

    # Sort by the compatibility score in descending order
    potential_matches = potential_matches.sort_values(by='compatibility_score', ascending=False)

    return potential_matches


# Rank the Potential Matches and Display the Top 5
def display_top_matches(potential_matches, top_n=5):
    top_matches = potential_matches[['user_id', 'name', 'location', 'age', 'compatibility_score']].head(top_n)
    print("Top Matches:")
    print(top_matches)
    return top_matches


# Select and Like a Match
def select_and_like_match(logged_in_user: User, selected_match_id):
    # Fetch the selected match as a User object
    selected_user = db.fetch_user(selected_match_id)
    # Use the User class's like method
    user_activities = UserActivities(logged_in_user.user_id)
    user_activities.add_liked_user(selected_user)

    # check if it is a match
    return selected_match_id in user_activities.view_matches()
