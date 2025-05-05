from app.Entities.user_profile import UserProfile

class ViewUserProfileController:
    def __init__(self):
        pass
        
    def getProfileById(self, profile_id):
        """
        Get user profile by ID
        
        Args:
            profile_id (int): ID of the profile to retrieve
            
        Returns:
            dict: Profile data or None if not found
        """
        try:
            profile = UserProfile.getUserProfileById(profile_id)
            
            if not profile:
                return None
                
            # Convert to dictionary for API response
            profile_dict = profile.to_dict()
            
            # Add user information
            from app.Entities.user import User
            print(f"[DEBUG] Attempting to get user with ID: {profile.user_id}")
            user = User.getUserById(profile.user_id)
            if user:
                profile_dict['username'] = user.username
                profile_dict['role'] = user.role
                profile_dict['status'] = user.status
                
            return profile_dict
            
        except Exception as e:
            print(f"[ViewUserProfileController] Error getting profile by ID: {str(e)}")
            import traceback
            print(f"[TRACE] {traceback.format_exc()}")
            return None
    
    def getProfileByUserId(self, user_id):
        """
        Get user profile by user ID
        
        Args:
            user_id (int): ID of the user whose profile to retrieve
            
        Returns:
            dict: Profile data or None if not found
        """
        try:
            profile = UserProfile.getUserProfileByUserId(user_id)
            
            if not profile:
                return None
                
            # Convert to dictionary for API response
            profile_dict = profile.to_dict()
            
            # Add user information
            from app.Entities.user import User
            print(f"[DEBUG] Attempting to get user with ID: {user_id}")
            user = User.getUserById(user_id)
            if user:
                profile_dict['username'] = user.username
                profile_dict['role'] = user.role
                profile_dict['status'] = user.status
                
            return profile_dict
            
        except Exception as e:
            print(f"[ViewUserProfileController] Error getting profile by user ID: {str(e)}")
            import traceback
            print(f"[TRACE] {traceback.format_exc()}")
            return None
    
    def getAllProfiles(self, user_id=None, full_name=None, phone=None):
        """
        Get all profiles with optional filtering
        
        Args:
            user_id (int, optional): Filter by user ID
            full_name (str, optional): Filter by full name (partial match)
            phone (str, optional): Filter by phone number (partial match)
            
        Returns:
            list: List of profiles matching the criteria
        """
        try:
            # Get filtered profiles
            profiles = UserProfile.filterProfiles(user_id, full_name, phone)
            
            if not profiles:
                return []
                
            # Convert to list of dictionaries for API response
            result = []
            for profile in profiles:
                profile_dict = profile.to_dict()
                
                # Add user information
                from app.Entities.user import User
                user = User.getUserById(profile.user_id)
                if user:
                    profile_dict['username'] = user.username
                    profile_dict['role'] = user.role
                    profile_dict['status'] = user.status
                
                result.append(profile_dict)
                
            return result
            
        except Exception as e:
            print(f"[ViewUserProfileController] Error getting all profiles: {str(e)}")
            return []
