from flask import *
from app.Controllers.Login import LoginAuthController
from app.Controllers.Logout import LogoutController
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
    profile = data.get('profile', '')

    controller = LoginAuthController()
    result = controller.login(username, password)

    if not result.get("success"):
        return jsonify({
            "message": result.get("message", "Login failed"),
            "status": "error"
        }), 401 

    userProfile = result.get("profile")
    userId = result.get("userId")

    session["userProfile"] = userProfile
    session["userId"] = userId

    #Validate selected profile
    if profile and userProfile and profile != userProfile:
        return jsonify({
            "message": f"Access denied. You do not have {profile} privileges.",
            "status": "error"
        }), 403

    return jsonify({
        "message": result.get("message"),
        "status": "success",
        "profile": userProfile,
        "username": username,
        "userId": userId
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    controller = LogoutController()
    result = controller.logout()
    return jsonify(result), 200
