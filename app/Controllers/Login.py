from app.Entities.user import User

class LoginAuthController:

    def login(self, username, password):
        
        authResult = User.authenticate(username, password)
        if not authResult["success"]:
            return authResult 

        user = User.getUser(username)

        return {
            "success": True,
            "message": "Login successful",
            "profile": user.profileName,
            "userId": user.getId()
        }