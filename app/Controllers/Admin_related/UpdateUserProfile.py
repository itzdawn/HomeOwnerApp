from app.Entities.user_profile import UserProfile

class UpdateUserProfileController:
    def __init__(self):
        pass
        
    def updateUserProfile(self, profile_id, full_name=None, phone=None, address=None):
        """
        Update a user profile
        
        Args:
            profile_id (int): ID of the profile to update
            full_name (str, optional): New full name
            phone (str, optional): New phone number
            address (str, optional): New address
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Check if profile exists
            profile = UserProfile.getUserProfileById(profile_id)
            if not profile:
                return {"success": False, "message": "Profile not found"}
            
            # Update profile fields
            if full_name:
                profile.full_name = full_name
            if phone:
                profile.phone = phone
            if address is not None:  # Allow empty string for address
                profile.address = address
            
            # Save changes
            result = profile.save()
            
            if result:
                return {
                    "success": True, 
                    "message": "Profile updated successfully",
                    "profile": profile.to_dict()
                }
            else:
                return {"success": False, "message": "Failed to update profile"}
                
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
