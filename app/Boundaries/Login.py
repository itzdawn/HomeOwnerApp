from flask import *
from app.Controllers.LoginController import LoginAuthController
from functools import wraps

# Route protection decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if userRole exists in session
        if 'userRole' not in session:
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
    role = data.get('role', '').lower()  # Get role from form data and convert to lowercase

    controller = LoginAuthController()
    result = controller.login(username, password)
    
    if result is None:
        return jsonify({"message": "Unexpected error during login", "status": "error"}), 500
    
    
    if result[1] == 200:  # login success
        user_role = result[0].get("role", "") .lower()
        
        session['userRole'] = user_role #store user role in session to match the role of the user

        # Check if the requested role matches the actual user role from database
        if role and user_role and role != user_role:
            return jsonify({"message": f"Access denied. You do not have {role} privileges.", "status": "error"}), 403
            
        # Return success response with role information
        return jsonify({
            "message": "Login successful",
            "status": "success",
            "role": user_role,
            "username": username
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
