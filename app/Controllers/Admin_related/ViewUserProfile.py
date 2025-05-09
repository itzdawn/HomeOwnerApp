from app.Entities.userProfile import UserProfile

class ViewUserProfileController:
    def __init__(self):
        pass
    
    def getProfileById(self, profileId):
        userProfile = UserProfile.getProfileById(profileId)
        if userProfile:
            return userProfile.toDict()
        else:
            return None