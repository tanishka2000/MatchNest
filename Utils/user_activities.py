from flaskr.UserActivities import UserActivities
from flaskr.UserDatabase import UserDatabase
from flaskr.models import UserActivitiesModel

db_file = 'users.db'
active_user = int(input("Enter active user's user_id: "))
user_activities = UserActivities(UserActivitiesModel(user_id=active_user), db_file)
db = UserDatabase(db_file)

# user_activities.add_liked_user(UserActivitiesModel(user_id=3))
# user_activities.add_liked_user(UserActivitiesModel(user_id=4))
# user_activities.add_liked_user(UserActivitiesModel(user_id=5))
# user_activities.add_liked_user(UserActivitiesModel(user_id=6))
# user_activities.add_disliked_user(UserActivitiesModel(user_id=7))
# user_activities.add_disliked_user(UserActivitiesModel(user_id=8))
print(user_activities.liked_users)






