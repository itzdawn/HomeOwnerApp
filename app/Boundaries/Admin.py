from flask import Blueprint, request, jsonify
from app.Controllers.CreateUserController import CreateUserController
from app.Controllers.GetAllUsersController import GetAllUsersController

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

@admin_bp.route('/update-users', methods=['POST'])
def updateUser():
    pass