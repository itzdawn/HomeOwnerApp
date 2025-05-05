from app.Entities.user import User

class DeleteUserController:
    def __init__(self):
        pass
        
    def deleteUser(self, user_id):
        """
        Delete a user account
        
        Args:
            user_id (int): ID of the user to delete
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Check if user exists
            user = User.getUserById(user_id)
            if not user:
                return {"success": False, "message": "User not found"}
                
            # Check if user is Admin
            if user.role == "Admin":
                return {"success": False, "message": "Cannot delete Administrator account"}
            
            # Check for dependent records before deleting
            # For example, you might want to prevent deletion of users with active services
            
            # Delete associated profile first
            from app.Entities.user_profile import UserProfile
            profile = UserProfile.getUserProfileByUserId(user_id)
            if profile:
                profile.delete()
            
            # Delete user
            result = user.delete()
            
            if result:
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete user"}
                
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
