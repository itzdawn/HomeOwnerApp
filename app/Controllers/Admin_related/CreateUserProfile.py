from app.Entities.userProfile import UserProfile

class CreateUserProfileController:

    def createUserProfile(self, name, description, status):
        try:
            pendingProfile = UserProfile(name=name, description=description, status=status)
            return pendingProfile.createProfile()

        except Exception as e:
            print(f"Error creating user profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    
            