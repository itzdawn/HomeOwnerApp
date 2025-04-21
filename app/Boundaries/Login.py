from flask import *
from app.Controllers.LoginController import LoginAuthController

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    controller = LoginAuthController()
    result = controller.login(username, password)
    
    if result is None:
        return jsonify({"message": "Unexpected error during login", "status": "error"}), 500
    
    if result[1] == 200: #login success
        if result[0]["role"] == "Admin":
            return render_template('admin_profile.html', username=username)
    else:
        return jsonify(result[0]), result[1]  # Return error message and status
