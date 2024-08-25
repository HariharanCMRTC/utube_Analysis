from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Load the machine learning model
model = joblib.load('Model.pickle')

# Create SQLite database and table if they don't exist
def init_db():
    with sqlite3.connect('ytDatabase.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if name and email and message:
            with sqlite3.connect('ytDatabase.db') as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO contacts (name, email, message)
                    VALUES (?, ?, ?)
                ''', (name, email, message))
                conn.commit()
                flash('Your message has been sent successfully!', 'success')
                return redirect(url_for('contactus'))
        else:
            flash('All fields are required!', 'danger')

    return render_template('contact.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/predictor', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        # Retrieve the form data
        views = int(request.form['views'])
        dislikes = int(request.form['dislikes'])
        comments_count = int(request.form['comments_count'])
        genre = int(request.form['genre'])

        # Prepare the data for the model
        feature_array = np.array([[views, dislikes, comments_count, genre]])

        # Make prediction using the model
        prediction = model.predict(feature_array)[0]

        # Display the result on a new page
        return render_template('result.html', prediction=round(prediction))
    return render_template('predictor.html')

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5050)
