from flaskr.UserActivities import UserActivities
from flaskr.UserDatabase import UserDatabase

db_file = 'users.db'
active_user = 1
user_activities = UserActivities(active_user, db_file)
db = UserDatabase(db_file)

# user_activities.add_liked_user(3)
# # user_activities.add_liked_user(UserActivitiesModel(user_id=4))
# # user_activities.add_liked_user(UserActivitiesModel(user_id=5))
# # user_activities.add_liked_user(UserActivitiesModel(user_id=6))
# # user_activities.add_disliked_user(UserActivitiesModel(user_id=7))
# # user_activities.add_disliked_user(UserActivitiesModel(user_id=8))
# print(user_activities.fetch_user_activity(1).liked_users)
# print(user_activities.fetch_user_activity(1).liked_users)
#
# # user2 = user_activities.liked_users[0]
# user_activities2 = UserActivities(3, db_file)
#
# user_activities2.add_liked_user(1)
# # user_activities2.add_liked_user(UserActivitiesModel(user_id=2))
# # user_activities2.add_liked_user(UserActivitiesModel(user_id=5))
# # user_activities2.add_liked_user(UserActivitiesModel(user_id=6))
# # user_activities2.add_disliked_user(UserActivitiesModel(user_id=9))
# # user_activities2.add_disliked_user(UserActivitiesModel(user_id=10))
# print(user_activities2.fetch_user_activity(3).liked_users)
#
# print(user_activities.fetch_user_activity(1).matches)
# print(user_activities2.fetch_user_activity(3).matches)




