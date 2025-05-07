from app.Entities.userProfile import UserProfile

class ViewUserProfileController:
    def __init__(self):
        pass

    def getAllProfiles(self):
        """
        Returns a list of all user profiles (id, name, description, status)
        """
        return UserProfile.getAllProfiles()
    
    def getProfileById(self, profileId):
       return UserProfile.getProfileById(profileId).toDict()
    