import os
import requests

# Constants for gender
MALE = "Male"
FEMALE = "Female"
NON_BINARY = "Non-binary"
OTHER = "Other"
PREFER_NOT_TO_SAY = "Prefer not to say"


# Function to get the gender-specific avatar URL
def get_avatar_url(gender, firstname):
    gender_map = {
        MALE: "boy",
        NON_BINARY: "boy",
        FEMALE: "girl",
        OTHER: "girl",
        PREFER_NOT_TO_SAY: "girl"
    }
    gender_key = gender_map.get(gender, "girl")
    return f"https://avatar.iran.liara.run/public/{gender_key}?username={firstname}" or ""


# Function to download and save the image to a folder
def download_and_save_avatar(url, firstname, folder_path):
    response = requests.get(url)
    if response.status_code == 200:
        image_path = os.path.join(folder_path, f"{firstname}.png")
        image_path= image_path.replace('\\', '/')
        print(image_path)
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)
        print(f"Avatar for {firstname} saved successfully at {image_path}.")
    else:
        print(f"Failed to download avatar for {firstname}. HTTP Status: {response.status_code}")


# Function to process user data and save avatars
def save_avatars(firstname, gender, folder_path='../static/profile_pics'):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    url = get_avatar_url(gender, firstname)
    download_and_save_avatar(url, firstname, folder_path)
    return firstname

