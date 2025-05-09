from app.Entities.user import User

class UpdateUserController:
    def __init__(self):
        pass
        
    def updateUser(self, userId, username=None, profile=None, status=None, password=None):
        """
        Update a user account
        
        Args:
            userId (int): ID of the user to update
            username (str, optional): New username
            profile (str, optional): New profile
            status (int, optional): New status (0=inactive, 1=active)
            password (str, optional): New password (if being changed)
            
        Returns:
            dict: Response with status and message
        """
        try:
            #check if user exists
            user = User.getUserById(userId)
            if not user:
                return {"success": False, "message": "User not found"}
            
            #protect system admin accounts
            if user.profileName == "Admin" and profile != "Admin":
                return {"success": False, "message": "Cannot change profile of Administrator account"}
            
            #check if username already exists (if changing username)
            if username and username != user.username:
                existingUser = User.getUser(username)
                if existingUser and existingUser.getId() != userId:
                    return {"success": False, "message": "Username already exists"}
            
            #Update user fields
            if username:
                user.username = username
            if profile:
                user.profileId = user.getProfileIndex(profile)
            if status is not None:
                user.status = status
            if password:
                user.setPassword(password)
            
            result = user.updateUser()
            
            if result:
                return {"success": True, "message": "User updated successfully"}
            else:
                return {"success": False, "message": "Failed to update user"}
                
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
