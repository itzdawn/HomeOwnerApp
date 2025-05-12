from flask import session

class LogoutController:
    def logout(self):
        session.clear()
        return {"message": "Logout successful", "status": "success"}