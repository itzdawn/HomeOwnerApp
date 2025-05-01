from flask import Blueprint, request, jsonify, render_template
from app.Controllers.Admin_related.CreateUser import CreateUserController
from app.Controllers.Admin_related.GetAllUsers import GetAllUsersController
from app.Boundaries.Login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create-user', methods=['POST'])
@login_required
def createUser():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    status = int(data.get('status'))
    
    controller = CreateUserController()
    response = controller.createUser(username, password, role, status)
    
    return jsonify(response)

@admin_bp.route('/display-users', methods=['GET'])
@login_required
def getAllUsers():
    controller = GetAllUsersController()
    users = controller.getAllUsers()
    return jsonify(users)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('LayoutIndex/AdminIndex.html')

@admin_bp.route('/user-accounts', methods=['GET'])
@login_required
def user_accounts():
    return render_template('UserAdminPage/user-account.html')

@admin_bp.route('/user-profiles', methods=['GET'])
@login_required
def user_profiles():
    return render_template('UserAdminPage/user-profile.html')

@admin_bp.route('/update-users', methods=['POST'])
@login_required
def updateUser():
    pass