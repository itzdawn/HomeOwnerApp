from app.Entities.user import User

class LoginAuthController():
    def __init__(self):
        pass
    
    def login(self, username, password):
        user = User.getUser(username)
        
        if user is None:
            return {"message": "Invalid Credentials", "status": "error"}, 401
        
        if user.getPassword() != password:
            return {"message": "Invalid Credentials", "status": "error"}, 401
        
        if user.status == 0:  # Assuming 0 means inactive, 1 means active
            return {"message": "Account Suspended", "status": "error"}, 403
            
        return {"message": "Login Success", "role": user.role}, 200

    
    
