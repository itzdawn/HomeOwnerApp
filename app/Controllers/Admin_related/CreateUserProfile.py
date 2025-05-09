from app.Entities.userProfile import UserProfile

class CreateUserProfileController:
    def __init__(self):
        pass
        
    def createUserProfile(self, name, description, status):
        try:
            if UserProfile.isNameTaken(name):
                return {"success": False, "message": "Profile name already exists"}
            profile = UserProfile(
                    name=name,
                    description=description,
                    status=status
                )
            response = profile.createProfile()
            if response:
                return {"success": True, "message": "Profile created successfully"}
            else:
                return {"success": False, "message": "Unable to create profile."}
        except Exception as e:
            print(f"Error creating user profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    
            