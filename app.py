from datetime import datetime

from flask import Flask, render_template, jsonify
from pydantic import ValidationError

from Utils.utils import get_zodiac_sign
from flaskr.UserDatabase import UserDatabase
from flaskr.matching_algorithm import compute_compatibility_scores
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

from flaskr.models import User, Gender, Options, ZodiacSign, MBTITypes, UserIdentifiers, UserActivitiesModel

app = Flask(__name__, template_folder='templates')

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


active_user = 1
db_file = './utils/users.db'
db = UserDatabase()
current_user = UserActivitiesModel(user_id=active_user)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def submit_details():
    return render_template('signup.html')

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
    return render_template('dashboard.html', recommendations = recommendations)


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
                           MBTITypes=MBTITypes)


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
    app.run(host="0.0.0.0", port=8000, debug=True)
