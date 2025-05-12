from app.Entities.user import User

class LoginAuthController:

    def login(self, username, password):
        if not User.authenticate(username, password):
            return {"success": False, "message": "Invalid credentials or suspended account"}

        user = User.getUser(username)

        return {
            "success": True,
            "message": "Login successful",
            "profile": user.profileName,
            "userId": user.getId()
        }