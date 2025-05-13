from app.Entities.userProfile import UserProfile

class SearchUserProfileController:
    def __init__(self):
        pass

    def searchProfiles(self, profileId=None, name=None):
        try:
            profiles = UserProfile.searchProfiles(profileId, name)
            return [p.toDict() for p in profiles]
        except Exception as e:
            print(f"Error retrieving user profiles: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
        
    def getAllProfiles(self):
        try:
            profiles = UserProfile.getAllProfiles()
            return [p.toDict() for p in profiles]
        except Exception as e:
            print(f"[Error]: unable to retrieve user profiles: {str(e)}")
            return []