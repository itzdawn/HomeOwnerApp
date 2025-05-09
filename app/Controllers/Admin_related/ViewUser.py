from app.Entities.user import User

class ViewUserController:
    def __init__(self):
        pass
    
    def getUserById(self, userId):
        user = User.getUserById(userId)
        if user:
            return user.toDict() 
        else:
            return None
    