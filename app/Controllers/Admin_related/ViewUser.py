from app.Entities.user import User

class ViewUserController:
    def __init__(self):
        pass
        
    def getUserById(self, user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): ID of the user to retrieve
            
        Returns:
            dict: User data or None if not found
        """
        try:
            user = User.getUserById(user_id)
            
            if not user:
                return None
                
            # Convert to dictionary for API response (exclude password)
            user_dict = user.to_dict()
            
            # Check if user has a profile
            from app.Entities.user_profile import UserProfile
            profile = UserProfile.getUserProfileByUserId(user_id)
            if profile:
                user_dict['has_profile'] = True
                user_dict['profile_id'] = profile.id
            else:
                user_dict['has_profile'] = False
                
            return user_dict
            
        except Exception as e:
            print(f"[ViewUserController] Error getting user by ID: {str(e)}")
            return None
    
    def getAllUsers(self, user_id=None, username=None, role=None, status=None):
        """
        Get all users with optional filtering
        
        Args:
            user_id (int, optional): Filter by user ID
            username (str, optional): Filter by username (partial match)
            role (str, optional): Filter by role
            status (int, optional): Filter by status
            
        Returns:
            list: List of users matching the criteria
        """
        try:
            # Get filtered users
            users = User.filterUsers(user_id, username, role)
            
            if not users:
                return []
                
            # Convert to list of dictionaries for API response
            result = []
            for user in users:
                # Filter by status if specified
                if status is not None and user.status != status:
                    continue
                    
                # Exclude password from response
                user_dict = user.to_dict()
                
                # Check if user has a profile
                from app.Entities.user_profile import UserProfile
                profile = UserProfile.getUserProfileByUserId(user.getId())
                if profile:
                    user_dict['has_profile'] = True
                    user_dict['profile_id'] = profile.id
                else:
                    user_dict['has_profile'] = False
                
                result.append(user_dict)
                
            return result
            
        except Exception as e:
            print(f"[ViewUserController] Error getting all users: {str(e)}")
            return []
