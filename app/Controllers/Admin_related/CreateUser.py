from app.Entities.user import User

class CreateUserController():

    #returns a dict    
    def createUser(self, username, password, profile, status):
        try:
            pendingUser = User(username=username, password=password, profileName=profile, status=status)
            return pendingUser.createUser()
        
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
