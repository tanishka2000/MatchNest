from flaskr.UserActivities import UserActivities

db_file = 'C:\\Users\\crite\\PycharmProjects\\MatchNest\\storage\\user_act.db'
active_user = 68
user_activities = UserActivities(db_file)
# db = UserDatabase(db_file)

user_activities.add_liked_user(active_user, 101)
user_activities.add_liked_user(active_user, 100)
user_activities.add_liked_user(active_user, 22)
# user_activities.add_liked_user(UserActivitiesModel(user_id=4))
# user_activities.add_liked_user(UserActivitiesModel(user_id=5))
# user_activities.add_liked_user(UserActivitiesModel(user_id=6))
# user_activities.add_disliked_user(UserActivitiesModel(user_id=7))
# user_activities.add_disliked_user(UserActivitiesModel(user_id=8))
# print("user_activities.fetch_user_activity(1).liked_users",user_activities.fetch_user_activity(1).liked_users)
# print("matches1: " ,user_activities.fetch_user_activity(1).matches)
#
# # user2 = user_activities.liked_users[0]
# user_activities2 = UserActivities(db_file)
#
# user_activities2.add_liked_user(3, 1)
# user_activities2.add_liked_user(UserActivitiesModel(user_id=2))
# user_activities2.add_liked_user(UserActivitiesModel(user_id=5))
# user_activities2.add_liked_user(UserActivitiesModel(user_id=6))
# user_activities2.add_disliked_user(UserActivitiesModel(user_id=9))
# user_activities2.add_disliked_user(UserActivitiesModel(user_id=10))
# print(user_activities2.fetch_user_activity(3).liked_users)
#
print(user_activities.fetch_user_activity(active_user).matches)
# print(user_activities2.fetch_user_activity(3).matches)




