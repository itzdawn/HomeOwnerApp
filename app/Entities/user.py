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
    
    @staticmethod
    def getUserById(user_id):
        """
        Retrieve a user by their ID from the database
        
        Args:
            user_id (int): The ID of the user to retrieve
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            # Ensure user_id is handled as an integer
            user_id_int = int(user_id)
            print(f"[DEBUG] Retrieving user with ID: {user_id_int}")
            
            cursor.execute("SELECT * FROM user WHERE id = ?", (user_id_int,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                print(f"[DEBUG] User found: ID={result[0]}, Username={result[1]}")
                return User(id=result[0], username=result[1], password=result[2], role=result[3], status=result[4])
            else:
                print(f"[DEBUG] No user found with ID: {user_id_int}")
                return None
        except Exception as e:
            print(f"[ERROR] Error retrieving user by ID: {str(e)}")
            import traceback
            print(f"[TRACE] {traceback.format_exc()}")
            return None
    
    @staticmethod
    def filterUsers(user_id=None, username=None, role=None):
        """
        Filter users based on criteria
        
        Args:
            user_id (int, optional): Filter by user ID
            username (str, optional): Filter by username (partial match)
            role (str, optional): Filter by role
            
        Returns:
            list: List of User objects matching the criteria
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            query = "SELECT * FROM user WHERE 1=1"
            params = []
            
            if user_id:
                query += " AND id = ?"
                params.append(user_id)
                
            if username:
                query += " AND username LIKE ?"
                params.append(f"%{username}%")
                
            if role:
                query += " AND role = ?"
                params.append(role)
                
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            users = []
            for result in results:
                user = User(id=result[0], username=result[1], password=result[2], role=result[3], status=result[4])
                users.append(user)
                
            return users
        except Exception as e:
            print(f"Error filtering users: {str(e)}")
            return []
            
    def to_dict(self):
        """
        Convert user object to dictionary (for API responses)
        
        Returns:
            dict: User data dictionary (excluding password)
        """
        return {
            'id': self.getId(),
            'username': self.username,
            'role': self.role,
            'status': self.status
        }
    
    def save(self):
        """
        Save or update user in database
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            if self.__id:  # Update existing user
                cursor.execute("""
                    UPDATE user 
                    SET username = ?, role = ?, status = ?
                    WHERE id = ?
                """, (self.username, self.role, self.status, self.__id))
            else:  # Create new user
                cursor.execute("""
                    INSERT INTO user (username, password, role, status)
                    VALUES (?, ?, ?, ?)
                """, (self.username, self.__password, self.role, self.status))
                self.__id = cursor.lastrowid
                
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            return False
    