from app.Entities.userProfile import UserProfile

class UpdateUserProfileController:
    def __init__(self):
        pass
        
    def updateUserProfile(self, id, name=None, description=None, status=None):
       profile = UserProfile.getProfileById(id)
       if name:
           profile.name = name
       if description:
           profile.description = description
       if status is not None:
           profile.status = status
       profile.updateProfile()
       
       return {"success": True, "message": "Profile updated successfully"}

