from app.Entities.user import User

class UpdateUserController:
    def __init__(self):
        pass
        
    def updateUser(self, user_id, username=None, role=None, status=None, password=None):
        """
        Update a user account
        
        Args:
            user_id (int): ID of the user to update
            username (str, optional): New username
            role (str, optional): New role
            status (int, optional): New status (0=inactive, 1=active)
            password (str, optional): New password (if being changed)
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Check if user exists
            user = User.getUserById(user_id)
            if not user:
                return {"success": False, "message": "User not found"}
            
            # Protect system admin accounts
            if user.role == "Admin" and role != "Admin":
                return {"success": False, "message": "Cannot change role of Administrator account"}
            
            # Check if username already exists (if changing username)
            if username and username != user.username:
                existing_user = User.getUserByUsername(username)
                if existing_user and existing_user.id != user_id:
                    return {"success": False, "message": "Username already exists"}
            
            # Update user fields
            if username:
                user.username = username
            if role:
                user.role = role
            if status is not None:
                user.status = status
            if password:
                import hashlib
                # Hash password (simple example - use a more secure method in production)
                user.password = hashlib.sha256(password.encode()).hexdigest()
            
            # Save changes
            result = user.save()
            
            if result:
                return {"success": True, "message": "User updated successfully"}
            else:
                return {"success": False, "message": "Failed to update user"}
                
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
