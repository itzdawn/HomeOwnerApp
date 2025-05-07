import sqlite3
from flask import current_app

def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class User:
    def __init__(self, username=None, password=None, profileId=None, status=None, id=None):
        self.__id = id
        self.username = username
        self.__password = password
        self.profileId = profileId
        self.status = status
        self.profileName = None #store profile name here for easier access.

    def setPassword(self, password):
        self.__password = password
    def getPassword(self):
        return self.__password
    def getId(self):
        return self.__id
    
    #insert new user to database
    def createUser(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password, profile_id, status) VALUES (?, ?, ?, ?)", 
                       (self.username, self.getPassword(), self.profileId, self.status))
        conn.commit()
        conn.close()
    def toDict(self):
        return {
            'id': self.getId(),
            'username': self.username,
            'profile': self.profileName,
            'status': self.status
        }
    
    def updateUser(self):
        try:
            conn = getDb()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE user 
                SET username = ?, password = ?, profile_id = ?, status = ?
                WHERE id = ?
            """, (self.username, self.getPassword(), self.profileId, self.status, self.getId()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False
    @staticmethod
    def isValidName(username):
        return len(username) > 0 #ensures username must contain at least 1 character.
    @staticmethod
    def isValidPass(password):
        return len(password) >= 7
    @staticmethod
    def isUsernameTaken(username):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result == None:
            return False
        else:
            return True 
    @staticmethod  
    def getAllUsers():
        conn = getDb()
        c = conn.cursor()
        c.execute("""SELECT user.id, user.username, user.status, user_profile.name 
                FROM user
                JOIN user_profile
                ON user.profile_id = user_profile.id""")
        users = c.fetchall() 
        conn.close()
        
        userList = []
        for user in users:
            userInfo = {
                'id': user[0],  #user id
                'username': user[1],  #username
                'profile': user[3],  #profile
                'status': user[2]
            }
            userList.append(userInfo)
        return userList
    
    @staticmethod
    def getProfileIndex(profile):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user_profile WHERE name = ?", (profile,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
        
    #retrieve user info from db
    @staticmethod
    def getUser(username):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("""SELECT user.id, user.username, user.password, user.profile_id, user.status, user_profile.name 
                        FROM user
                        JOIN user_profile
                        ON user.profile_id = user_profile.id
                        WHERE user.username = ?""", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user = User(id=result[0], username=result[1], password=result[2], profileId=result[3], status=result[4])
            user.profileName = result[5]
            return user
        else:
            return None 
    @staticmethod
    def getUserById(userId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            userIdInt = int(userId)
            cursor.execute("""SELECT user.id, user.username, user.password, user_profile.id, user.status, user_profile.name
                        FROM user
                        JOIN user_profile
                        ON user_profile.id = user.profile_id
                        WHERE user.id = ?""", (userIdInt,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user = User(id=result[0], username=result[1], password=result[2], profileId=result[3], status=result[4])
                user.profileName = result[5]
                return user
            else:
                return None
        except Exception as e:
            print(f"[ERROR] Error retrieving user by ID: {str(e)}")
            return None
    
    
    #return a list of user objects as according to criteria
    @staticmethod
    def searchUsers(userId=None, username=None, profile=None):
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            query = """SELECT user.id, user.username, user.password, user.profile_id, user.status, user_profile.name
                FROM user JOIN user_profile
                ON user.profile_id = user_profile.id WHERE 1=1"""
            params = []
            
            if userId:
                query += " AND user.id = ?"
                params.append(userId)
                
            if username:
                query += " AND user.username LIKE ?"
                params.append(f"%{username}%")
                
            if profile:
                query += " AND user_profile.name = ?"
                params.append(profile)
                    
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            users = []
            for result in results:
                user = User(
                    id=result[0],
                    username=result[1],
                    password=result[2],
                    profileId=result[3],
                    status=result[4]
                )
                user.profileName = result[5]
                users.append(user)
            return users
        
        except Exception as e:
            print(f"Error filtering users: {str(e)}")
            return []
            
    