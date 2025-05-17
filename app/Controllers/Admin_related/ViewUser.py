from app.Entities.user import User

class ViewUserController:
    def getUserById(self, userId):
        return User.getUserById(userId).toDict()
    