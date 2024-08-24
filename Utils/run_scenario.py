from flaskr.UserDatabase import UserDatabase
from flaskr.matching_algorithm import compute_compatibility_scores

db = UserDatabase()
# Step 1: Simulate user login
logged_in_user_id = int(input("Enter your user ID to log in: "))
logged_in_user = db.fetch_user(logged_in_user_id)
if logged_in_user is None:
    print("User ID not found. Exiting.")

print('Logged in successfully. Variables of the logged in user: ', vars(logged_in_user))

# Step 2: Load all users into a DataFrame
all_users_df = db.fetch_all_users()

like_number = 0
# users get to select whether exit or not
close = False

# Step 3: Loop until the user likes someone
while True:
    # Compute and rank top matches based on compatibility score
    if close:
        break

    if like_number == 25:
        print("You have reached your daily like limits")
        break

    potential_matches = compute_compatibility_scores(logged_in_user, all_users_df)

    if potential_matches.empty:
        print("No more potential matches found. Exiting.")
        break

    # Display the top match
    top_match = potential_matches.iloc[0]
    print(f"\nTop Match: {top_match['name']}, Age: {top_match['age']}, Location: {top_match['location']}")
    print(f"Shared Interests: {', '.join(top_match['interests'])}")
    print(f"Compatibility Score: {top_match['compatibility_score']:.2f}")

    # Get user's decision
    decision = input("Do you want to like or dislike this user? (like/dislike): ").strip().lower()

    if decision == "like":
        # The user likes the top match
        selected_match_id = int(top_match['user_id'])
        select_and_like_match(logged_in_user, selected_match_id)
        all_users_df = all_users_df[all_users_df['user_id'] != selected_match_id]
        print(f"You liked {top_match['name']}. Match has been made! Exiting.")
        like_number += 1
    elif decision == "dislike":
        # The user dislikes the top match
        disliked_match_id = int(top_match['user_id'])
        logged_in_user.disliked_users.append(disliked_match_id)
        # Remove the disliked match from potential matches and continue looping
        all_users_df = all_users_df[all_users_df['user_id'] != disliked_match_id]
        print(f"You disliked {top_match['name']}. Moving on to the next match...")
    else:
        print("Invalid input. Please type 'like' or 'dislike'.")

# Step 4: Update and display the logged-in user's profile
update_and_display_user_profile(logged_in_user)