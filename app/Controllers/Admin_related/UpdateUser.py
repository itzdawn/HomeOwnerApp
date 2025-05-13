from app.Entities.user import User

class UpdateUserController:

    def updateUser(self, userId, username=None, profileName=None, status=None, password=None):
        try:
            #check if user exists
            user = User.getUserById(userId)
            if not user:
                return {"success": False, "message": "User not found"}
            
            #protect system admin accounts
            if user.profileName == "Admin" and profileName != "Admin":
                return {"success": False, "message": "Cannot change profile of Administrator account"}
            
            #check if username already exists (if changing username)
            if username and username != user.username:
                existingUser = User.getUser(username)
                if existingUser and existingUser.getId() != userId:
                    return {"success": False, "message": "Username already exists"}
            
            #Update user fields if all validation is ok.
            return user.updateUser(username=username, password=password, profileName=profileName, status=status )

        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
