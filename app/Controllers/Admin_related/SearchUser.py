from app.Entities.user import User

class SearchUserController:
    def __init__(self):
        pass

    def searchUsers(self, userId=None, username=None, profile=None):
        try:
            users = User.searchUsers(userId, username, profile)
            return [u.toDict() for u in users]
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    #return all list of all users.    
    def getAllUsers(self):
        try:
            return User.getAllUsers()
        except Exception as e:
            print(f"[Error] Unable to retrieve user: {str(e)}")
            return []