from app.Entities.userProfile import UserProfile

class ViewUserProfileController:
    def __init__(self):
        pass
    
    def getProfileById(self, profileId):
        return UserProfile.getProfileById(profileId).toDict()
