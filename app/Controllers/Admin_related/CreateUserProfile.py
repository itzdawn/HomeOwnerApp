from app.Entities.userProfile import UserProfile

class CreateUserProfileController:
    def __init__(self):
        pass
        
    def createUserProfile(self, name, description, status):
        if UserProfile.isNameTaken(name):
            return {"success": False, "message": "Profile name already exists"}
        profile = UserProfile(
                name=name,
                description=description,
                status=status
            )
        profile.createProfile()
        return {"success": True, "message": "Profile created successfully"}
 
            