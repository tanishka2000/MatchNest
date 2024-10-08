from flaskr.models import MBTITypes

MBTI_PAIRS = {
    "ENFJ": ["INFP"],
    "ENTJ": ["INFP"],
    "INFJ": ["ENFP"],
    "INTJ": ["ENFP"],
    "ENTP": ["INFJ", "INTJ"],
    "ISFP": ["ENFJ", "ESFJ", "ESTJ"],
    "ISTP": ["ESTJ", "ESFJ"],
    "ESTJ": ["ISFP", "ISTP"],
    "ESFJ": ["ISFP", "ISTP"],
    "ISTJ": ["ESFP"],
    "ISFJ": ["ESFP"]
}

ZODIAC_COMPATIBILITY = {
    ('Aries', 'Aries'): 0.50,
    ('Aries', 'Taurus'): 0.38,
    ('Aries', 'Gemini'): 0.83,
    ('Aries', 'Cancer'): 0.42,
    ('Aries', 'Leo'): 0.97,
    ('Aries', 'Virgo'): 0.63,
    ('Aries', 'Libra'): 0.85,
    ('Aries', 'Scorpio'): 0.50,
    ('Aries', 'Sagittarius'): 0.93,
    ('Aries', 'Capricorn'): 0.47,
    ('Aries', 'Aquarius'): 0.78,
    ('Aries', 'Pisces'): 0.67,
    ('Taurus', 'Taurus'): 0.65,
    ('Taurus', 'Gemini'): 0.33,
    ('Taurus', 'Cancer'): 0.97,
    ('Taurus', 'Leo'): 0.73,
    ('Taurus', 'Virgo'): 0.90,
    ('Taurus', 'Libra'): 0.65,
    ('Taurus', 'Scorpio'): 0.88,
    ('Taurus', 'Sagittarius'): 0.30,
    ('Taurus', 'Capricorn'): 0.98,
    ('Taurus', 'Aquarius'): 0.58,
    ('Taurus', 'Pisces'): 0.85,
    ('Gemini', 'Gemini'): 0.60,
    ('Gemini', 'Cancer'): 0.65,
    ('Gemini', 'Leo'): 0.88,
    ('Gemini', 'Virgo'): 0.68,
    ('Gemini', 'Libra'): 0.93,
    ('Gemini', 'Scorpio'): 0.28,
    ('Gemini', 'Sagittarius'): 0.60,
    ('Gemini', 'Capricorn'): 0.68,
    ('Gemini', 'Aquarius'): 0.85,
    ('Gemini', 'Pisces'): 0.53,
    ('Cancer', 'Cancer'): 0.75,
    ('Cancer', 'Leo'): 0.35,
    ('Cancer', 'Virgo'): 0.90,
    ('Cancer', 'Libra'): 0.43,
    ('Cancer', 'Scorpio'): 0.94,
    ('Cancer', 'Sagittarius'): 0.53,
    ('Cancer', 'Capricorn'): 0.90,
    ('Cancer', 'Aquarius'): 0.27,
    ('Cancer', 'Pisces'): 0.98,
    ('Leo', 'Leo'): 0.45,
    ('Leo', 'Virgo'): 0.35,
    ('Leo', 'Libra'): 0.97,
    ('Leo', 'Scorpio'): 0.58,
    ('Leo', 'Sagittarius'): 0.97,
    ('Leo', 'Capricorn'): 0.58,
    ('Leo', 'Aquarius'): 0.35,
    ('Leo', 'Pisces'): 0.38,
    ('Virgo', 'Virgo'): 0.65,
    ('Virgo', 'Libra'): 0.68,
    ('Virgo', 'Scorpio'): 0.88,
    ('Virgo', 'Sagittarius'): 0.48,
    ('Virgo', 'Capricorn'): 0.95,
    ('Virgo', 'Aquarius'): 0.30,
    ('Virgo', 'Pisces'): 0.88,
    ('Libra', 'Libra'): 0.75,
    ('Libra', 'Scorpio'): 0.35,
    ('Libra', 'Sagittarius'): 0.73,
    ('Libra', 'Capricorn'): 0.55,
    ('Libra', 'Aquarius'): 0.90,
    ('Libra', 'Pisces'): 0.88,
    ('Scorpio', 'Scorpio'): 0.88,
    ('Scorpio', 'Sagittarius'): 0.35,
    ('Scorpio', 'Capricorn'): 0.95,
    ('Scorpio', 'Aquarius'): 0.28,
    ('Scorpio', 'Pisces'): 0.97,
    ('Sagittarius', 'Sagittarius'): 0.48,
    ('Sagittarius', 'Capricorn'): 0.60,
    ('Sagittarius', 'Aquarius'): 0.90,
    ('Sagittarius', 'Pisces'): 0.63,
    ('Capricorn', 'Capricorn'): 0.95,
    ('Capricorn', 'Aquarius'): 0.55,
    ('Capricorn', 'Pisces'): 0.88,
    ('Aquarius', 'Aquarius'): 0.68,
    ('Aquarius', 'Pisces'): 0.45,
    ('Pisces', 'Pisces'): 0.60,
}

LOCATIONS = ["New York", "Boston", "Chicago", "San Francisco", "Los Angeles"]
INTERESTS_POOL = ["hiking", "reading", "movies", "gaming", "cooking", "music", "traveling", "photography",
                  "fitness", "yoga"]
PROFESSION_POOL = [
    "Software Developer", "Data Scientist", "IT Consultant", "Cybersecurity Analyst", "Network Engineer",
    "Systems Administrator", "Database Administrator", "Web Developer", "UX/UI Designer", "Mobile App Developer",
    "Nurse", "Physician", "Dentist", "Pharmacist", "Physical Therapist", "Occupational Therapist",
    "Medical Laboratory Technician", "Radiologic Technologist", "Health Information Technician", "Paramedic",
    "Teacher", "Professor", "School Counselor", "Educational Administrator", "Librarian", "Special Education Teacher"]
BIO_POOL = [
    "Adventure enthusiast and coffee lover. Always looking for the next great story.",
    "Tech geek by day, musician by night. Living life one code at a time.",
    "Traveling the world one country at a time. Passionate about new cultures and experiences.",
    "Fitness fanatic with a love for cooking healthy meals. Let’s share recipes!",
    "Bookworm and movie buff. I believe every day is an opportunity to learn something new.",
    "Dreamer and doer, always striving to make the world a better place.",
    "Cat lover, coffee addict, and a fan of all things creative. Let's create something beautiful together.",
    "Avid gamer and tech enthusiast. I love exploring new technologies and their potential.",
    "Dog parent and nature lover. I find peace in the great outdoors.",
    "Artist at heart, marketing professional by trade. I see beauty in everything.",
    "Foodie and aspiring chef. I enjoy experimenting with new recipes and flavors.",
    "Yoga enthusiast with a passion for mindfulness and meditation.",
    "History buff and amateur photographer. Capturing the world one snapshot at a time.",
    "Music lover with an eclectic taste. Always on the lookout for new tunes.",
    "Environmental advocate and nature lover. Dedicated to making a difference.",
    "Writer by passion, editor by profession. Words are my playground.",
    "Entrepreneur with a creative spirit. Always working on the next big idea.",
    "Science nerd with a fascination for the universe. Let's explore the cosmos together.",
    "Social butterfly with a love for hosting and connecting with people.",
    "DIY enthusiast and home decorator. I believe every space can be transformed into a sanctuary."
]
MBTI_POOL = tuple(mbti.value for mbti in MBTITypes)
