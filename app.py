from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import bcrypt

#region App Setup
app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = os.urandom(20)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./backend/Arkham.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

FASTAPI_URL = "http://127.0.0.1:8000"

@app.route('/', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        response = requests.get(f"{FASTAPI_URL}/users")
        
        if response.status_code == 200:
            users = response.json()

            user = next((u for u in users if u["username"] == username), None)
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Error connecting to backend.', 'danger')
            return render_template('login.html')

# @app.route('/home')
# def home():

# @app.route('/register')
# def register():

# @app.route('message')
# def messages():



# if __name__ == "__main__":
#     app.run(debug=True)