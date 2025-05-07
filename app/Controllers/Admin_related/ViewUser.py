from app.Entities.user import User

class ViewUserController:
    def __init__(self):
        pass
    
    def getAllUsers(self):
        """
        Controller wrapper for getting all users (for display)
        
        Returns:
            list: List of user dicts with id, username, profile, and status
        """
        try:
            users = User.getAllUsers()
            return users
        except Exception as e:
            print(f"[ViewUserController] Error retrieving users: {str(e)}")
            return []
    
    def getUserById(self, userId):
        user = User.getUserById(userId)
        if user:
            return user.toDict() 
        else:
            return None
    