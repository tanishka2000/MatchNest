import hashlib
import os
import secrets
import sqlite3

import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from flask import jsonify, session, flash
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from flaskr.UserDatabase import UserDatabase
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


active_user = 1
user_cred_db_file = './storage/user_cred.db'
db_file = './utils/users.db'
db = UserDatabase()
current_user = UserActivitiesModel(user_id=active_user)


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
            db.insert_new_user(User(
                user_id=new_user_id,
                name=name
            ))
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
            session['user_id'] = user[0]
            flash('Login successful!', 'info')
            return jsonify({"success": True})

        else:
            flash('Invalid email or password.', 'error')

        conn.close()

        return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


def fetch_logged_in_user_id():
    print(session.get('user_id', 1))
    return session.get('user_id', 1)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # db.setup_database()
    logged_in_user = db.fetch_user(active_user)
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
    recommendations = potential_matches.head(25).to_dict(orient='records')
    return render_template('dashboard.html', recommendations=recommendations)


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
    user = db.fetch_user(user_id)

    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404

    if request.method == 'POST':
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            print(file)
            if file and allowed_file(file.filename):
                # Secure the filename and save it
                filename = secure_filename(file.filename)
                filename = user.name.split(' ')[0]
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print("FILE:", file_path, filename)
                user.profile_pic = filename

        updated_data = {
            "user_id": user.user_id,
            "name": request.form.get('name', user.name),
            "profile_pic": user.profile_pic,
            "bio": request.form.get('bio', user.bio),
            "birth_date": request.form.get('birth_date', user.birth_date),
            "zodiac_sign": request.form.get('zodiac_sign', user.zodiac_sign),
            "gender": request.form.get('gender', user.gender),
            "profession": request.form.get('profession', user.profession),
            "location": request.form.get('location', user.location),
            "smoking": request.form.get('smoking', user.smoking),
            "drinking": request.form.get('drinking', user.drinking),
            "interests": request.form.get('interests').split(',') if request.form.get('interests') else user.interests,
            "mbti": request.form.get('mbti', user.mbti),
            "height": int(request.form.get('height', user.height)),
        }

        try:
            updated_user = UserIdentifiers(**updated_data)
            db.update_account(updated_user)
            return jsonify({"success": True})
        except ValidationError as e:
            return jsonify({"success": False, "error": str(e)}), 400

    return render_template('registerProfile.html',
                           user=user,
                           Gender=Gender,
                           Options=Options,
                           ZodiacSign=ZodiacSign,
                           MBTITypes=MBTITypes, fetch_logged_in_user_id=fetch_logged_in_user_id)


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def display_profile(user_id=1):
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
    matches = db.fetch_matches(active_user)
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


if __name__ == '__main__':
    db = UserDatabase()
    init_user_cred(user_cred_db_file)
    app.run(host="0.0.0.0", port=8000, debug=True)
