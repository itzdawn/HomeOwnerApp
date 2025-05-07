from flask import *
from app.Controllers.LoginController import LoginAuthController
from functools import wraps

# Route protection decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if userProfile exists in session
        if 'userProfile' not in session:
            # Redirect to login page if not logged in
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    
    data = request.form
    username = data.get('username')
    password = data.get('password')
    profile = data.get('profile', '')  # Get profile from form data 

    controller = LoginAuthController()
    result = controller.login(username, password)
    
    if result is None:
        return jsonify({"message": "Unexpected error during login", "status": "error"}), 500
    
    
    if result[1] == 200:  # login success
        userProfile = result[0].get("profile", "")  # Get original case profile from DB
        userId = result[0].get("userId", "")  # Get user ID from DB result
        
        session['userProfile'] = userProfile  # Store user profile in session with original case
        session['userId'] = userId  # Store user ID in session

        # Check if the requested profile matches the actual user profile from database
        if profile and userProfile and profile != userProfile:
            return jsonify({"message": f"Access denied. You do not have {profile} privileges.", "status": "error"}), 403
            
        # Return success response with profile information
        return jsonify({
            "message": "Login successful",
            "status": "success",
            "profile": userProfile,  # Send original case profile
            "username": username,
            "userId": userId  # Include user ID in response
        }), 200
    else:
        # Return error message and status
        return jsonify(result[0]), result[1]

@auth_bp.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    # Redirect to the login page (index route)
    return redirect(url_for('index'))
