from app.Entities.user import User

class SearchUserController:
    def __init__(self):
        pass

    def searchUsers(self, userId=None, username=None, profile=None):
        users = User.searchUsers(userId, username, profile)
        return [u.toDict() for u in users]
