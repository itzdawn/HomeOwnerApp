import sqlite3
from flask import current_app

def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class User:
    def __init__(self, username=None, password=None, role=None, status=None, id=None):
        self.__id = id
        self.username = username
        self.__password = password
        self.role = role
        self.status = status

    def isValidName(self):
        return len(self.username) > 0 #ensures username must contain at least 1 character.
    
    def isValidPass(self):
        return len(self.__password) >= 7
    
    def getPassword(self):
        return self.__password
    
    def getId(self):
        return self.__id
    
    #retrieve user info from db
    @staticmethod
    def getUser(username):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return User(id=result[0], username=result[1], password=result[2], role=result[3], status=result[4])
        else:
            return None 
    
    #insert new user to database
    def createUser(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password, role, status) VALUES (?, ?, ?, ?)", 
                       (self.username, self.__password, self.role, self.status))
        conn.commit()
        conn.close()
    
    def isUsernameTaken(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (self.username,))
        result = cursor.fetchone()
        conn.close()
        
        if result == None:
            return False
        else:
            return True 
        
    def getAllUsers(self):
        conn = getDb()
        c = conn.cursor()
        c.execute("SELECT id, username, role, status FROM user")
        users = c.fetchall() 
        conn.close()
        
        userList = []
        for user in users:
            userInfo = {
                'id': user[0],  #user id
                'username': user[1],  #username
                'role': user[2],  #role
                'status': 'Active' if user[3] == 1 else 'Suspended'
            }
            userList.append(userInfo)
        return userList
    