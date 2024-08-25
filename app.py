import hashlib
import os
import secrets
import sqlite3

import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from flask import jsonify, flash
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from Utils.utils import get_zodiac_sign
from flaskr.UserDatabase import UserDatabase
from flaskr.active_user import active_user, end_user_session, fetch_active_user, is_user_authenticated
from flaskr.matching_algorithm import compute_compatibility_scores
from flaskr.models import User, Gender, Options, ZodiacSign, MBTITypes, UserIdentifiers, UserActivitiesModel
from flaskr.storage import init_user_cred

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


active_user_id = 1
user_cred_db_file = './storage/user_cred.db'
db_file = './utils/users.db'
db = UserDatabase()
current_user = UserActivitiesModel(user_id=active_user_id)


@app.route('/')
def index():
    return render_template('index.html')


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = hash_password(request.form.get('password'))
        print(name, email, password)
        if not name or not email or not password:
            return jsonify({'success': False, 'error': 'Missing data 1'}), 400

        conn = sqlite3.connect(user_cred_db_file)
        cursor = conn.cursor()

        last_user_id = db.get_last_user_id()
        new_user_id = last_user_id + 1

        try:
            cursor.execute('INSERT INTO user_cred (user_id, name, email, password) VALUES (?, ?, ?, ?)',
                           (new_user_id, name, email, password))
            conn.commit()
            response = {'success': True, 'user_id': new_user_id}

            active_user(new_user_id)
            return jsonify(response)

        except sqlite3.IntegrityError:
            response = {'success': False, 'error': 'Email already registered.'}
            return jsonify(response)
        except Exception as e:
            response = {'success': False, 'error': str(e)}
            return jsonify(response)
        finally:
            conn.close()
    return render_template('signup.html', fetch_logged_in_user_id=fetch_logged_in_user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect(user_cred_db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM user_cred WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            active_user(user[0])
            print('Login successful!', 'info')
            return jsonify({"success": True})
        else:
            jsonify({"success": False, "error": "Invalid Credentials"})

        conn.close()
        return render_template('index.html')


@app.route('/logout')
def logout():
    end_user_session()
    flash('You have been logged out.')
    return redirect('/')


def fetch_logged_in_user_id():
    return fetch_active_user()


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not is_user_authenticated():
        return redirect(url_for('login'))
    # db.setup_database()
    active_user_id = fetch_logged_in_user_id()
    print("User", active_user_id)
    logged_in_user = db.fetch_user(active_user_id)
    print(logged_in_user)
    if logged_in_user is None:
        print("User ID not found. Exiting.")
    print(logged_in_user)
    # Step 2: Load all users into a DataFrame
    all_users_df = db.fetch_all_users()
    columns = [
        'user_id', 'name', 'birth_date', 'age', 'gender', 'location',
        'interests', 'smoking', 'drinking', 'zodiac_sign', 'mbti',
        'profession', 'height', 'bio', 'profile_pic'
    ]

    # Convert the list of tuples to a DataFrame
    df = pd.DataFrame(all_users_df, columns=columns)
    potential_matches = compute_compatibility_scores(logged_in_user, df)
    # Convert DataFrame to a list of dictionaries
    recommendations = potential_matches.head(25).to_dict(orient='records')

    # Process each recommendation
    for recommendation in recommendations:
        # Convert the interests field from string to list if necessary
        if isinstance(recommendation.get('interests'), str):
            recommendation['interests'] = [interest.strip() for interest in recommendation['interests'].split(',')]

    return render_template('dashboard.html', recommendations=recommendations)


@app.context_processor
def inject_user_id_image():
    logged_in_user = db.fetch_user(fetch_logged_in_user_id())
    if logged_in_user:
        user_profile_pic_url = f"/static/profile_pics/{logged_in_user.profile_pic}" if logged_in_user.profile_pic else "https://via.placeholder.com/40"
        return dict(fetch_logged_in_user_id=fetch_logged_in_user_id, user_profile_pic_url=user_profile_pic_url)
    return dict(fetch_logged_in_user_id=fetch_logged_in_user_id)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, browser also submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Here, save the filename or file path to the user's record in the database
            # Example: save_user_image(logged_in_user_id, filename)

            return redirect(url_for('upload_file', filename=filename))

    return render_template('upload.html')


@app.route('/profile/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id=1):
    if not is_user_authenticated():
        return redirect(url_for('login'))

    # Check if the user exists
    user = db.fetch_user(user_id)

    if request.method == 'POST':
        # Initialize filename
        filename = None

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                # Secure the filename and save it
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

        # If filename is an empty string, use the existing profile_pic
        profile_pic = filename if filename and filename.strip() != "" else (user.profile_pic if user else None)

        # Collect updated data from the form
        updated_data = {
            "user_id": user_id,  # Use provided user_id
            "name": request.form.get('name', user.name if user else ''),
            "profile_pic": profile_pic,
            "bio": request.form.get('bio', user.bio if user else ''),
            "birth_date": request.form.get('dob', user.birth_date if user else ''),
            "zodiac_sign": request.form.get('zodiac_sign', user.zodiac_sign if user else ''),
            "gender": request.form.get('gender', user.gender if user else ''),
            "profession": request.form.get('profession', user.profession if user else ''),
            "location": request.form.get('location', user.location if user else ''),
            "smoking": request.form.get('smoking', user.smoking if user else ''),
            "drinking": request.form.get('drinking', user.drinking if user else ''),
            "interests": request.form.get('interests', ',').split(',') if request.form.get('interests') else (
                user.interests if user else []),
            "mbti": request.form.get('mbti', user.mbti if user else ''),
            "height": int(request.form.get('height', user.height if user else 0)),
        }

        try:
            # If user is None, it's a new user. Otherwise, it's an existing user.
            if user is None:
                new_user = UserIdentifiers(**updated_data)
                db.insert_new_user(new_user)  # Insert new user into DB
            else:
                updated_user = UserIdentifiers(**updated_data)
                db.update_account(updated_user)  # Update existing user

            return jsonify({"success": True})
        except ValidationError as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # Render form with blank fields for new users or existing user data
    return render_template('registerProfile.html',
                           user=user,
                           Gender=Gender,
                           Options=Options,
                           ZodiacSign=ZodiacSign,
                           MBTITypes=MBTITypes,
                           fetch_logged_in_user_id=fetch_logged_in_user_id)


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def display_profile(user_id=1):
    if not is_user_authenticated():
        return redirect(url_for('login'))
    user = db.fetch_user(user_id)

    if not user:
        return "User not found", 404

    if request.method == 'POST':
        if 'profile_pic' not in request.files:
            return redirect(request.url)

        try:
            return redirect(url_for('display_profile', user_id=user_id))
        except ValidationError as e:
            return f"Error: {e}", 400

    return render_template('personalProfile.html',
                           user=user)


@app.route('/matches', methods=['GET', 'POST'])
def display_matches():
    if not is_user_authenticated():
        return redirect(url_for('login'))
    matches = db.fetch_matches(active_user_id)
    print(matches)
    matched_users = []

    if matches:
        matched_users = [db.fetch_user(matched_id) for matched_id in matches]
    return render_template('viewMatches.html',
                           matched_users=matched_users)


@app.route('/like', methods=['POST'])
def like_user():
    data = request.get_json()
    user_id = data.get('user_id')
    # Assuming current_user_id is retrieved from session or request
    current_user_id = 1  # Replace with actual user ID

    if not user_id:
        return jsonify({'error': 'Missing user ID'}), 400

    # Fetch the user to like
    db.add_liked_users(current_user_id, user_id)
    return jsonify({'status': 'success'}), 200


@app.route('/dislike', methods=['POST'])
def dislike_user():
    data = request.get_json()
    user_id = data.get('user_id')
    # Assuming current_user_id is retrieved from session or request
    current_user_id = 1  # Replace with actual user ID

    if not user_id:
        return jsonify({'error': 'Missing user ID'}), 400

    # Fetch the user to dislike
    db.add_disliked_users(current_user_id, user_id)
    return jsonify({'status': 'success'}), 200


@app.route('/get_zodiac_sign', methods=['POST'])
def calculate_zodiac():
    dob = request.json.get('dob')
    if dob:
        zodiac_sign = get_zodiac_sign(dob)
        return jsonify({"success": True, 'zodiac_sign': zodiac_sign})
    return jsonify({'error': 'Invalid date of birth'}), 400

if __name__ == '__main__':
    db = UserDatabase()
    init_user_cred(user_cred_db_file)
    app.run(host="0.0.0.0", port=8000, debug=True)
