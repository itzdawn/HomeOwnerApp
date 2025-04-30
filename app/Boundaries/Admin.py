from flask import Blueprint, request, jsonify, render_template
from app.Controllers.Admin_related.CreateUser import CreateUserController
from app.Controllers.Admin_related.GetAllUsers import GetAllUsersController

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create-user', methods=['POST'])
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
def getAllUsers():
    controller = GetAllUsersController()
    users = controller.getAllUsers()
    return jsonify(users)

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('LayoutIndex/AdminIndex.html')

@admin_bp.route('/user-accounts', methods=['GET'])
def user_accounts():
    return render_template('UserAdminPage/user-account.html')

@admin_bp.route('/user-profiles', methods=['GET'])
def user_profiles():
    return render_template('UserAdminPage/user-profile.html')

@admin_bp.route('/update-users', methods=['POST'])
def updateUser():
    pass