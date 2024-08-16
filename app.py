from flask import Flask, render_template
from flaskr.UserDatabase import UserDatabase
from flaskr.matching_algorithm import compute_compatibility_scores
import pandas as pd
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__, template_folder='templates')
active_user = 1
db = UserDatabase()

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
        'interests', 'smoking', 'drinking', 'constellation', 'mbti',
        'profession', 'height', 'bio'
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


if __name__ == '__main__':
    db = UserDatabase()
    app.run(debug=True)
