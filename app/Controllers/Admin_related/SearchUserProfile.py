from app.Entities.userProfile import UserProfile

class SearchUserProfileController:
    def __init__(self):
        pass

    def searchProfiles(self, profileId=None, name=None):
        profiles = UserProfile.searchProfiles(profileId, name)
        return [p.toDict() for p in profiles]