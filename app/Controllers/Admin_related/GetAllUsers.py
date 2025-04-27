from app.Entities.user import User

class GetAllUsersController():
    def __init__(self):
        self.user = User()
    
    def getAllUsers(self):
        users = self.user.getAllUsers()
        return users
    
       
    