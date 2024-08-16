import random
from datetime import datetime, timedelta

user_modifiable_fields = ['bio', 'img', 'gender', 'profession', 'smoking', 'drinking', 'interests', 'mbti']

def random_birth_date(start_year=1970, end_year=2006):
    # Randomly select a year between start_year and end_year
    year = random.randint(start_year, end_year)

    # Randomly select a day of the year
    start_date = datetime(year, 1, 1)
    random_days = random.randint(0, 364)  # 0 to 364 days
    random_date = start_date + timedelta(days=random_days)

    # Return the date in "YYYY-MM-DD" format
    return random_date.strftime('%Y-%m-%d')

def calculate_age(dob):
    """Calculates age based on date of birth."""
    dob = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age

def get_zodiac_sign(dob):
    """Determines the zodiac sign based on date of birth."""
    dob = datetime.strptime(dob, "%Y-%m-%d")
    zodiac_signs = [
        ("Capricorn", (datetime(dob.year, 12, 22), datetime(dob.year, 1, 19))),
        ("Aquarius", (datetime(dob.year, 1, 20), datetime(dob.year, 2, 18))),
        ("Pisces", (datetime(dob.year, 2, 19), datetime(dob.year, 3, 20))),
        ("Aries", (datetime(dob.year, 3, 21), datetime(dob.year, 4, 19))),
        ("Taurus", (datetime(dob.year, 4, 20), datetime(dob.year, 5, 20))),
        ("Gemini", (datetime(dob.year, 5, 21), datetime(dob.year, 6, 20))),
        ("Cancer", (datetime(dob.year, 6, 21), datetime(dob.year, 7, 22))),
        ("Leo", (datetime(dob.year, 7, 23), datetime(dob.year, 8, 22))),
        ("Virgo", (datetime(dob.year, 8, 23), datetime(dob.year, 9, 22))),
        ("Libra", (datetime(dob.year, 9, 23), datetime(dob.year, 10, 22))),
        ("Scorpio", (datetime(dob.year, 10, 23), datetime(dob.year, 11, 21))),
        ("Sagittarius", (datetime(dob.year, 11, 22), datetime(dob.year, 12, 21))),
    ]

    for sign, (start, end) in zodiac_signs:
        if start <= dob <= end:
            return sign

    return "Capricorn" if dob.month == 1 and dob.day <= 19 else None