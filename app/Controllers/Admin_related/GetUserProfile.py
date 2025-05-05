from app.Entities.user_profile import UserProfile

class GetUserProfileController:
    def __init__(self):
        pass
        
    def getUserProfiles(self, user_id=None, full_name=None, phone=None):
        """
        Get user profiles with optional filtering
        
        Args:
            user_id (str, optional): Filter by user ID
            full_name (str, optional): Filter by full name (partial match)
            phone (str, optional): Filter by phone number (partial match)
            
        Returns:
            list: List of user profiles matching the criteria
        """
        try:
            print(f"[DEBUG] Getting profiles with filters - user_id: {user_id}, full_name: {full_name}, phone: {phone}")
            
            # Get all profiles with optional filtering
            profiles = UserProfile.filterProfiles(user_id, full_name, phone)
            
            # If no profiles found, return empty list
            if not profiles:
                print("[DEBUG] No profiles found with the given filters")
                return []
                
            # Convert profiles to dictionaries for JSON response
            result = []
            for profile in profiles:
                # Get user information
                from app.Entities.user import User
                print(f"[DEBUG] Getting user with ID {profile.user_id} for profile {profile.id}")
                user = User.getUserById(profile.user_id)
                
                profile_dict = profile.to_dict()
                
                # Add user information to the profile
                if user:
                    profile_dict['username'] = user.username
                    profile_dict['role'] = user.role
                    profile_dict['status'] = user.status
                else:
                    print(f"[WARNING] User not found for profile {profile.id} with user_id {profile.user_id}")
                
                result.append(profile_dict)
            
            print(f"[DEBUG] Returning {len(result)} profiles")
            return result
            
        except Exception as e:
            print(f"Error getting profiles: {str(e)}")
            import traceback
            print(f"[TRACE] {traceback.format_exc()}")
            return []
            
    def getUserProfileById(self, profile_id):
        """
        Get a specific user profile by ID
        
        Args:
            profile_id (int): ID of the profile to retrieve
            
        Returns:
            dict: User profile data or None if not found
        """
        try:
            profile = UserProfile.getUserProfileById(profile_id)
            
            if not profile:
                return None
                
            profile_dict = profile.to_dict()
            
            # Add user information
            from app.Entities.user import User
            user = User.getUserById(profile.user_id)
            if user:
                profile_dict['username'] = user.username
                profile_dict['role'] = user.role
                profile_dict['status'] = user.status
                
            return profile_dict
            
        except Exception as e:
            print(f"Error getting profile: {str(e)}")
            return None
