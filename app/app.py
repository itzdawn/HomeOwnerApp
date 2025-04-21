from flask import Flask, render_template, request, redirect, url_for, session

#import routes
from Boundaries.Login import auth_bp
from Boundaries.Admin import admin_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key in production

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')



@app.route('/')
def index():
    return render_template('login.html')

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)