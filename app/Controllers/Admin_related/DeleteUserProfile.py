from app.Entities.user_profile import UserProfile

class DeleteUserProfileController:
    def __init__(self):
        pass
        
    def deleteUserProfile(self, profile_id):
        """
        Delete a user profile
        
        Args:
            profile_id (int): ID of the profile to delete
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Check if profile exists
            profile = UserProfile.getUserProfileById(profile_id)
            if not profile:
                return {"success": False, "message": "Profile not found"}
            
            # Delete the profile
            result = profile.delete()
            
            if result:
                return {"success": True, "message": "Profile deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete profile"}
                
        except Exception as e:
            print(f"Error deleting profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
