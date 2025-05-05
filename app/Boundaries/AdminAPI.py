from flask import Blueprint, request, jsonify, session
from app.Controllers.Admin_related.CreateUser import CreateUserController
from app.Controllers.Admin_related.UpdateUser import UpdateUserController
from app.Controllers.Admin_related.DeleteUser import DeleteUserController
from app.Controllers.Admin_related.CreateUserProfile import CreateUserProfileController
from app.Controllers.Admin_related.UpdateUserProfile import UpdateUserProfileController
from app.Controllers.Admin_related.DeleteUserProfile import DeleteUserProfileController
from app.Controllers.Admin_related.ViewUser import ViewUserController
from app.Controllers.Admin_related.ViewUserProfile import ViewUserProfileController
from app.Boundaries.Login import login_required

# Blueprint for all admin API endpoints
admin_api_bp = Blueprint('admin_api', __name__)

# User account endpoints

@admin_api_bp.route('/users', methods=['GET'])
@login_required
def get_users_api():
    try:
        # Get filter parameters
        user_id = request.args.get('user_id')
        username = request.args.get('username')
        role = request.args.get('role')
        status = request.args.get('status')
        if status:
            status = int(status)
        
        controller = ViewUserController()
        users = controller.getAllUsers(user_id, username, role, status)
        
        return jsonify(users)
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_by_id_api(user_id):
    try:
        controller = ViewUserController()
        user = controller.getUserById(user_id)
        
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users', methods=['POST'])
@login_required
def create_user_api():
    try:
        data = request.json or request.form
        
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        status = int(data.get('status', 1))
        
        controller = CreateUserController()
        response = controller.createUser(username, password, role, status)
        
        if response.get('success'):
            return jsonify(response), 201
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user_api(user_id):
    try:
        data = request.json or request.form
        
        controller = UpdateUserController()
        response = controller.updateUser(
            user_id=user_id,
            username=data.get('username'),
            role=data.get('role'),
            status=int(data.get('status', 1))
        )
        
        if response.get('success'):
            return jsonify(response)
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user_api(user_id):
    try:
        controller = DeleteUserController()
        response = controller.deleteUser(user_id)
        
        if response.get('success'):
            return jsonify(response)
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

# User profile API endpoints

@admin_api_bp.route('/profiles', methods=['GET'])
@login_required
def get_profiles_api():
    try:
        # Get filter parameters
        user_id = request.args.get('user_id')
        full_name = request.args.get('full_name')
        phone = request.args.get('phone')
        
        controller = ViewUserProfileController()
        profiles = controller.getAllProfiles(user_id, full_name, phone)
        
        return jsonify(profiles)
    except Exception as e:
        print(f"Error getting profiles: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles/<int:profile_id>', methods=['GET'])
@login_required
def get_profile_by_id_api(profile_id):
    try:
        controller = ViewUserProfileController()
        profile = controller.getProfileById(profile_id)
        
        if profile:
            return jsonify(profile)
        else:
            return jsonify({"error": "Profile not found"}), 404
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_profile_by_user_id_api(user_id):
    try:
        controller = ViewUserProfileController()
        profile = controller.getProfileByUserId(user_id)
        
        if profile:
            return jsonify(profile)
        else:
            return jsonify({"error": "Profile not found for this user"}), 404
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles', methods=['POST'])
@login_required
def create_profile_api():
    try:
        data = request.json or request.form
        
        controller = CreateUserProfileController()
        response = controller.createUserProfile(
            user_id=data.get('user_id'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        if response.get('success'):
            return jsonify(response), 201
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error creating profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles/<int:profile_id>', methods=['PUT'])
@login_required
def update_profile_api(profile_id):
    try:
        data = request.json or request.form
        
        controller = UpdateUserProfileController()
        response = controller.updateUserProfile(
            profile_id=profile_id,
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        if response.get('success'):
            return jsonify(response)
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles/<int:profile_id>', methods=['DELETE'])
@login_required
def delete_profile_api(profile_id):
    try:
        controller = DeleteUserProfileController()
        response = controller.deleteUserProfile(profile_id)
        
        if response.get('success'):
            return jsonify(response)
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error deleting profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500 