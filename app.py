from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key in production
DB_FILE = 'users.db'

# --- Initialize SQLite DB and Add Admin/User ---
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
            )
        ''')
        users = [
            ('admin', 'admin123', 'admin'),
            ('alice01', 'pass123', 'user'),
            # ... (your full list of users)
            ('yuki50', 'user210', 'user')
        ]
        c.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)
        conn.commit()
        conn.close()

# --- Validate Login Credentials ---
def validate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# --- Login Page ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = validate_user(username, password)
        if user:
            session['user'] = user[0]
            session['role'] = user[1]
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# --- Profile Redirect Based on Role ---
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    if session['role'] == 'admin':
        return render_template('admin_profile.html', username=username)
    else:
        return render_template('user_profile.html', username=username)

# --- Add New User (Admin Only) ---
@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))  # Only admins can add users
    
    new_username = request.form['new_username'].strip()
    new_password = request.form['new_password'].strip()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  (new_username, new_password, 'user'))
        conn.commit()
        return redirect(url_for('profile'))  # Success: redirect back to admin dashboard
    except sqlite3.IntegrityError:
        conn.close()
        return render_template('admin_profile.html', username=session['user'], 
                              error='Username already taken. Try another.')
    finally:
        conn.close()

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Run App ---
if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        init_db()
    app.run(debug=True)