from app.Entities.user import User

class CreateUserController():
    def __init__(self):
        pass
        
    def createUser(self, username, password, role, status):
        newUser = User(username, password, role, status)
        if not newUser.isValidName():
            return {"message": "Invalid username", "status": "error"}
        
        if not newUser.isValidPass():
            return {"message": "Password must be at least 7 characters long", "status": "error"}
        
        if newUser.isUsernameTaken():
            return {"message": "Username already taken", "status": "error"}
        
        newUser.save()
        return {"message": f"User {username} created successfully", "status": "success"}
    