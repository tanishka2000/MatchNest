from enum import Enum

class Options(str, Enum):
    NEVER = "Never"
    SOMETIMES = "Sometimes"
    ALWAYS = "Always"

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

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    OTHER = "Other"
    PREFER_NOT_TO_SAY = "Prefer not to say"

class Smoking(str, Enum):
    NEVER = "Never"
    SOMETIMES = "Sometimes"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"

class Drinking(str, Enum):
    NEVER = "Never"
    OCCASIONALLY = "Occasionally"
    SOCIALLY = "Socially"
    FREQUENTLY = "Frequently"
    ALWAYS = "Always"
