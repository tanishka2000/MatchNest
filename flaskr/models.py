from pydantic import BaseModel, ValidationError, Field, validator
from typing import List, Optional
from enum import Enum

#Define the class gender with necessary attributes
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"

#Define the class Options with necessary attributes
class Options(str, Enum):
    NEVER = "Never"
    OCCASIONALLY = "Occasionally"
    SOCIALLY = "Socially"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"

#Define the class ZodiacSign with necessary attributes
class ZodiacSign(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

#Define the class MBTITypes with necessary attributes
class MBTITypes(str, Enum):
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"

#Define the class UserPreferenceFields with necessary attributes
class UserPreferenceFields(BaseModel):
    age: List[int]
    gender: List[Gender]

#Define the class UserDetails with necessary attributes

class UserActivitiesModel(BaseModel):
    user_id: int
    liked_users: Optional[list] = []
    disliked_users: Optional[ list] = []
    matches: Optional[list] = []


class UserDetails(BaseModel):
    location: str
    smoking: Options
    drinking: Options
    interests: List[str]
    zodiac_sign: Optional[ZodiacSign]
    mbti: MBTITypes
    height: int


class UserIdentifiers(UserDetails):
    user_id: Optional[int] = Field(default=None, description="Unique ID for the user. Auto-incremented in the database.")
    name: str
    bio: str
    birth_date: str
    gender: Gender
    profession: str
    profile_pic: str = ""

#Define the class User(BaseModel) with necessary attributes
class User(BaseModel):
    user_id: int
    name: str
    bio: str
    birth_date: str
    gender: Gender
    profession: str
    location: str
    smoking: Options
    age: Optional[int]
    zodiac_sign: Optional[ZodiacSign]
    drinking: Options
    interests: List[str]
    mbti: MBTITypes
    height: int
    profile_pic: str = ""


def get_user_input() -> UserIdentifiers:
    try:
        user_data = {
            "user_id": int(input("Enter User ID: ")),
            "name": input("Enter Name: "),
            "bio": input("Enter Bio: "),
            "profile_pic": input("Enter path to your profile pic: "),
            "birth_date": input("Enter Date of Birth (YYYY-MM-DD): "),
            "gender": input(f"Enter Gender ({', '.join([g.value for g in Gender])}): "),
            "profession": input("Enter Profession: "),
            "location": input("Enter Location: "),
            "smoking": input(f"Enter Smoking Habit ({', '.join([o.value for o in Options])}): "),
            "drinking": input(f"Enter Drinking Habit ({', '.join([o.value for o in Options])}): "),
            "interests": input("Enter Interests (comma-separated): ").split(','),
            "mbti": input(f"Enter MBTI ({', '.join([mbti.value for mbti in MBTITypes])}): "),
            "height": int(input("Enter Height (in cm): "))
        }

        user = UserIdentifiers(**user_data)
        return user

    except ValidationError as e:
        print(f"Error: {e}")
        return None
