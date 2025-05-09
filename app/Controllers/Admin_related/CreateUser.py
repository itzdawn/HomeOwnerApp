from app.Entities.user import User

class CreateUserController():
    def __init__(self):
        pass
    #returns a dict    
    def createUser(self, username, password, profile, status):
        try:
            pendingUser = User()
            if not pendingUser.isValidName(username):
                return {"message": "Invalid username", "status": "error"}
            if not pendingUser.isValidPass(password):
                return {"message": "Password must be at least 7 characters long", "status": "error"}
            if pendingUser.isUsernameTaken(username):
                return {"message": "Username already taken", "status": "error"}
            profileId = pendingUser.getProfileIndex(profile)
            newUser = User(username, password, profileId, status)
            response = newUser.createUser()
            if response:
                return {"message": f"User: {username} created successfully", "success": True}
            else:
                return {"message": f"Unable to create User: {username}", "success": False}
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
