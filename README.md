# MatchNest - A Flask-Based Dating App

**MatchNest** is a dating application built using Flask, SQLite3, CSS, JavaScript, and HTML. The app allows users to
create profiles, upload images, and swipe through potential matches similar to popular dating apps like Tinder. The
application focuses on delivering personalized user recommendations based on user preferences and compatibility scores.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Compatibility Scoring](#compatibility-scoring)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Authentication (Signup, Login)
- Profile Management (Edit Bio, Preferences, Image Upload)
- Swipe Interface for Matching
- Compatibility Scoring Based on Bio and Interests
- Flask Backend with SQLite3 Database
- Responsive Frontend using CSS and JavaScript
- Image Upload and Display

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite3
- Node.js (for frontend development)

### Setup

## Project Setup

Here’s the complete Markdown file with all the bash commands included:

```markdown
# MatchNest

This project is designed to help users find compatible matches based on various factors such as location, age, interests, and more.

## Project Setup

Follow the steps below to set up and run the project locally:

### 1. Clone the Repository

To get started, clone the repository from GitHub and navigate into the project directory:

```bash
git clone https://github.com/yourusername/matchnest.git
cd matchnest
```

### 2. Install Python Dependencies

Install the required Python dependencies by running the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages listed in the `requirements.txt` file.

### 3. Run Flask

Start the Flask development server to run the application:

```bash
flask run
```

Once the server is running, you can access the application in your web browser at `http://127.0.0.1:5000/`.

## Bash Commands Summary

Below is a summary of all the bash commands used in this project setup:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/matchnest.git
    ```

2. **Navigate into the project directory:**

    ```bash
    cd matchnest
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Flask:**

    ```bash
    flask run
    ```

## Features

- User registration and authentication
- Profile creation and editing
- Matching algorithm based on various compatibility factors
- Display of potential matches with options to like or dislike
- User interaction management, including likes, dislikes, and matches

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```

This Markdown file includes all the bash commands used in the project setup, providing a clear and concise guide for users to get the project up and running.

### Usage

Sign Up: Create a new account using the signup form.
Login: Use your credentials to log in.
Update Profile: Add a bio, upload a profile picture, and set preferences.
Swipe: Browse through recommended profiles and swipe left or right.
Matches: View your matches and start interacting.

### Database Schema

The application uses SQLite3 for data persistence. The following tables are defined:

**users:** Stores user details like user_id, name, bio, location, etc.
**user_preferences:** Stores user preferences like age range, gender preference, etc.
**user_activities:** Tracks liked, disliked, and matched users.

### Compatibility Scoring

The app calculates compatibility scores based on:

**Bio-Bio Matching**: Compare user bios to find common keywords.
**Interests-Interests Matching**: Compare user interests.
**Bio-Interests Matching**: Compare bio keywords with the other user's interests and vice versa.
**Location Matching**: Scores based on proximity.
**Age Difference**: Scores based on age differences.

These scores are used to recommend the most compatible matches to users.
