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
- [Contact](#contact)

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

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/tanishka2000/MatchNest.git
   cd MatchNest
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**
   ```bash
   flask init-db
   ```

5. **Run the Application:**
   ```bash
   flask run
   ```
   Access the application at `http://127.0.0.1:5000/`.

## Usage

Sign Up: Create a new account using the signup form.
Login: Use your credentials to log in.
Update Profile: Add a bio, upload a profile picture, and set preferences.
Swipe: Browse through recommended profiles and swipe left or right.
Matches: View your matches and start interacting.

## Database Schema

The application uses SQLite3 for data persistence. The following tables are defined:

**users:** Stores user details like user_id, name, bio, location, etc.
**user_preferences:** Stores user preferences like age range, gender preference, etc.
**user_activities:** Tracks liked, disliked, and matched users.

## Compatibility Scoring

The app calculates compatibility scores based on:

**Bio-Bio Matching**: Compare user bios to find common keywords.
**Interests-Interests Matching**: Compare user interests.
**Bio-Interests Matching**: Compare bio keywords with the other user's interests and vice versa.
**Location Matching**: Scores based on proximity.
**Age Difference**: Scores based on age differences.

These scores are used to recommend the most compatible matches to users.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`feature/YourFeature`).
3. Commit your changes with clear messages.
4. Push to the branch.
5. Open a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For questions or support, please open an issue in this repository.
