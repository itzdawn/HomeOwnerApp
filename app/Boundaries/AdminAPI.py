from flask import Blueprint, request, jsonify
from app.Controllers.Admin_related.CreateUser import CreateUserController
from app.Controllers.Admin_related.UpdateUser import UpdateUserController
from app.Controllers.Admin_related.CreateUserProfile import CreateUserProfileController
from app.Controllers.Admin_related.UpdateUserProfile import UpdateUserProfileController
from app.Controllers.Admin_related.ViewUser import ViewUserController
from app.Controllers.Admin_related.ViewUserProfile import ViewUserProfileController
from app.Controllers.Admin_related.SearchUser import SearchUserController
from app.Controllers.Admin_related.SearchUserProfile import SearchUserProfileController
from app.Boundaries.Auth import login_required

admin_api_bp = Blueprint('admin_api', __name__)


#search and filter according to name/profile/id
@admin_api_bp.route('/users', methods=['GET'])
@login_required
def searchUsersApi():
    try:
        user_id = request.args.get('userId', type=int)
        username = request.args.get('username')
        profile = request.args.get('profile')
        controller = SearchUserController()
        if user_id or username or profile:
            users = controller.searchUsers(user_id, username, profile)
        else:
            users = controller.getAllUsers()
        return jsonify(users), 200
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        return jsonify({"error": "Server error"}), 500
    
#for viewing user details
@admin_api_bp.route('/users/<int:userId>', methods=['GET'])
@login_required
def getUserByIdApi(userId):
    try:
        controller = ViewUserController()
        user = controller.getUserById(userId)
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users', methods=['POST'])
@login_required
def createUserApi():
    try:
        data = request.json or request.form
        
        username = data.get('username')
        password = data.get('password')
        profile = data.get('profile')
        status = int(data.get('status', 1))
        
        controller = CreateUserController()
        response = controller.createUser(username, password, profile, status)
        if response.get('success'):
            return jsonify(response), 201
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/users/<int:userId>', methods=['PUT'])
@login_required
def updateUserApi(userId):
    try:
        data = request.json or request.form
        
        controller = UpdateUserController()
        response = controller.updateUser(
            userId=userId,
            username=data.get('username'),
            profileName=data.get('profile'),
            status=int(data.get('status', 1))
        )
        if response.get('success'):
            return jsonify(response), 200
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"error": "Server error"}), 500


# User profile API endpoints ----------------------------------------------------------------------------------------------------

@admin_api_bp.route('/profiles', methods=['GET'])
@login_required
def searchProfilesApi():
    try:
        profile_id = request.args.get('profile_id', type=int)
        name = request.args.get('name')
        controller = SearchUserProfileController()
        if profile_id or name:
            profiles = controller.searchProfiles(profile_id, name)
        else:
            profiles = controller.getAllProfiles()

        return jsonify(profiles), 200
    except Exception as e:
        print(f"Error getting profiles: {str(e)}")
        return jsonify({"error": "Server error"}), 500


@admin_api_bp.route('/profiles/<int:profileId>', methods=['GET'])
@login_required
def getProfileByIdApi(profileId):
    try:
        controller = ViewUserProfileController()
        profile = controller.getProfileById(profileId)
        
        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({"error": "Profile not found"}), 404
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles', methods=['POST'])
@login_required
def createProfileApi():
    try:
        data = request.json or request.form
        
        controller = CreateUserProfileController()
        response = controller.createUserProfile(
            name=data.get('name'),
            description=data.get('description'),
            status=int(data.get('status', 1))
        )
        
        if response.get('success'):
            return jsonify(response), 201
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error creating profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@admin_api_bp.route('/profiles/<int:profileId>', methods=['PUT'])
@login_required
def updateProfileApi(profileId):
    try:
        data = request.json or request.form
        
        controller = UpdateUserProfileController()
        response = controller.updateUserProfile(
            id=profileId,
            name=data.get('name'),
            description=data.get('description'),
            status=int(data.get('status', 1))
        )
        
        if response.get('success'):
            return jsonify(response), 200
        else:
            return jsonify(response), 400
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return jsonify({"error": "Server error"}), 500