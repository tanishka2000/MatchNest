# Setup the database and create 100 users
import random

from Utils.constants import LOCATIONS, INTERESTS_POOL, MBTI_POOL, PROFESSION_POOL, BIO_POOL
from Utils.generate_profile_pics import save_avatars
from Utils.utils import random_birth_date, calculate_age, get_zodiac_sign
from flaskr.UserDatabase import UserDatabase
from flaskr.models import User, Gender, Options

db = UserDatabase()
db.setup_database()

# Randomly generate 100 users with different attributes
for i in range(1, 101):
    name = f"User{i}"
    birth_date = random_birth_date()
    gender = random.choice([gender.value for gender in Gender])
    location = random.choice(LOCATIONS)
    interests = random.sample(INTERESTS_POOL, random.randint(2, 5))  # Each user has 2-5 interests
    mbti = random.choice(MBTI_POOL)
    smoking = random.choice([options.value for options in Options])
    drinking = random.choice([options.value for options in Options])
    profession = random.choice(PROFESSION_POOL)
    height = random.randint(140, 200)
    bio = random.choice(BIO_POOL)
    profile_pic = save_avatars(name, gender) + '.png'
    age = calculate_age(birth_date)
    zodiac_sign = get_zodiac_sign(birth_date)
    user = User(
        user_id=i,
        name=name,
        birth_date=birth_date,
        age=age,
        zodiac_sign=zodiac_sign,
        gender=gender,
        location=location,
        interests=interests,
        mbti=mbti,
        smoking=smoking,
        drinking=drinking,
        profession=profession,
        height=height,
        bio=bio,
        profile_pic=profile_pic)

    db.insert_new_user(user)
