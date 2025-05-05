import sqlite3
from app.Entities.user_profile import UserProfile

class CreateUserProfileController:
    def __init__(self):
        pass
        
    def createUserProfile(self, user_id, full_name, phone, address=None):
        """
        Create a new user profile
        
        Args:
            user_id (int): User ID to link profile to
            full_name (str): Full name of the user
            phone (str): Phone number of the user
            address (str, optional): Address of the user
            
        Returns:
            dict: Response with status and message
        """
        try:
            # Validate input
            if not user_id or not full_name or not phone:
                return {"success": False, "message": "Missing required fields"}
            
            # Check if user exists
            from app.Entities.user import User
            user = User.getUserById(user_id)
            if not user:
                return {"success": False, "message": "User not found"}
                
            # Check if profile already exists for user
            existing_profile = UserProfile.getUserProfileByUserId(user_id)
            if existing_profile:
                return {"success": False, "message": "Profile already exists for this user"}
            
            # Create new profile
            profile = UserProfile(
                user_id=user_id,
                full_name=full_name,
                phone=phone,
                address=address
            )
            
            # Save to database
            profile_id = profile.save()
            
            if profile_id:
                return {
                    "success": True, 
                    "message": "Profile created successfully",
                    "profile_id": profile_id
                }
            else:
                return {"success": False, "message": "Failed to create profile"}
                
        except Exception as e:
            print(f"Error creating profile: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
