import sqlite3
from flask import current_app

def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class User:
    def __init__(self, username=None, password=None, profileName=None, profileId=None, status=None, id=None):
        self.__id = id
        self.username = username
        self.__password = password
        self.profileId = profileId
        self.status = status
        self.profileName = profileName

    def setPassword(self, password):
        self.__password = password
    def getPassword(self):
        return self.__password
    def getId(self):
        return self.__id
    def toDict(self):
        return {
            'id': self.getId(),
            'username': self.username,
            'profile': self.profileName,
            'status': self.status
        }
    #methods for internal use---------------------------------------------------------------------------------
    
    #to derive profile index from profile name, prepares the proper data for creating user in db
    def _getProfileIndex(self, profileName):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user_profile WHERE name = ?", (profileName,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    def _isUsernameTaken(self, username):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return True
        else:
            return False
            
    
    
    #end of internal methods ------------------------------------------------------------------------------------------
    
    #basically uses created User's constructor to insert into db
    def createUser(self):
        try:
            if self._isUsernameTaken(self.username):
                return {"message": "Username already taken", "status": "error"}
            if self.profileId == None:
                self.profileId = self._getProfileIndex(self.profileName)
                if self.profileId is None:
                    return {"message": f"Invalid profile: {self.profileName}", "success": False}
            
            with getDb() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user (username, password, profile_id, status) VALUES (?, ?, ?, ?)", 
                            (self.username, self.getPassword(), self.profileId, self.status))
                conn.commit()
                
                #if insertion somehow didn't occur
                if cursor.rowcount == 0:
                    return {"message": f"Unable to create User: {self.username}", "success": False}
                else:
                    return {"message": f"User: {self.username} created successfully", "success": True}
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def updateUser(self, username=None, password=None, profileName=None, status=None):
        try:
            #use existing values if parameters are not provided
            username = username or self.username
            password = password or self.getPassword()
            profileId = self._getProfileIndex(profileName) or self.profileId
            status = status if status is not None else self.status
            
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user 
                SET username = ?, password = ?, profile_id = ?, status = ?
                WHERE id = ?
            """, (username, password, profileId, status, self.getId()))

            conn.commit()
            if cursor.rowcount == 0:
                conn.close()
                return {"success": False, "message": "No user was updated."}
            conn.close()
            return {"success": True, "message": "User updated successfully"}
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
    

    
    def authenticate(username, password):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT u.id, u.profile_id, u.status
                FROM user u
                WHERE u.username = ? AND u.password = ?
            """
            cursor.execute(query, (username, password))
            row = cursor.fetchone()
            conn.close()

            if not row:
                return {"success": False, "message": "Invalid username or password"}

            if row["status"] == 0:
                return {"success": False, "message": "Account is suspended"}

            return {"success": True, "message": "Authentication successful"}

        except Exception as e:
            print(f"[User.authenticate] Error: {e}")
            return {"success": False, "message": "Unexpected error occurred during authentication"}

    @staticmethod  
    def getAllUsers():
        try:
            conn = getDb()
            c = conn.cursor()
            c.execute("""SELECT user.id, user.username, user.password, user.status, user_profile.id, user_profile.name 
                    FROM user
                    JOIN user_profile
                    ON user.profile_id = user_profile.id""")
            users = c.fetchall() 
            conn.close()
            
            userList = []
            for user in users:
                userObj = User(
                    id=user[0],
                    username=user[1],
                    password=user[2],
                    profileId=user[4],
                    status=user[3],
                    profileName=user[5]
                )
                userList.append(userObj)
            return userList
        except Exception as e:
            print(f"[ERROR] Error retrieving users: {str(e)}")
            return None
        
    #retrieve user info from db, used by login controller.
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
            user = User(id=result[0], username=result[1], password=result[2], profileId=result[3], status=result[4], profileName=result[5])
            return user
        else:
            return None
        
    #for getting user (obj) from userId
    @staticmethod
    def getUserById(userId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            #to ensure userid is always int.
            userIdInt = int(userId)
            cursor.execute("""SELECT user.id, user.username, user.password, user_profile.id, user.status, user_profile.name
                        FROM user
                        JOIN user_profile
                        ON user_profile.id = user.profile_id
                        WHERE user.id = ?""", (userIdInt,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user = User(id=result[0], username=result[1], password=result[2], profileId=result[3], status=result[4], profileName=result[5])
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
                    status=result[4],
                    profileName = result[5]
                )
                users.append(user)
            return users
        
        except Exception as e:
            print(f"Error filtering users: {str(e)}")
            return []
            
    