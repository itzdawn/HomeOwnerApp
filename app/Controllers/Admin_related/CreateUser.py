from app.Entities.user import User

class CreateUserController():
    def __init__(self):
        pass
        
    def createUser(self, username, password, profile, status):
        pendingUser = User()
        if not pendingUser.isValidName(username):
            return {"message": "Invalid username", "status": "error"}
        
        if not pendingUser.isValidPass(password):
            return {"message": "Password must be at least 7 characters long", "status": "error"}
        
        if pendingUser.isUsernameTaken(username):
            return {"message": "Username already taken", "status": "error"}
        profileId = pendingUser.getProfileIndex(profile)
        newUser = User(username, password, profileId, status)
        newUser.createUser()
        return {"message": f"User {username} created successfully", "status": "success"}
    