from app.Entities.userProfile import UserProfile

class UpdateUserProfileController:
    def __init__(self):
        pass
        
    def updateUserProfile(self, id, name=None, description=None, status=None):
        try:
            profile = UserProfile.getProfileById(id)
            if name:
                profile.name = name
            if description:
                profile.description = description
            if status is not None:
                profile.status = status
            response = profile.updateProfile()
            if response:
                return {"success": True, "message": "Profile updated successfully"}
            else:
                return {"success": False, "message": "Failed to update user profile"}
        except Exception as e:
            print(f"Error updating user profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

        
       

