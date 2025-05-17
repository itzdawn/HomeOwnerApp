from app.Entities.userProfile import UserProfile

class UpdateUserProfileController:
    
    def updateUserProfile(self, id, name=None, description=None, status=None):
        try:
            profile = UserProfile.getProfileById(id)
            return profile.updateProfile(name=name, description=description, status=status)
        except Exception as e:
            print(f"Error updating user profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

        
       

