import sqlite3
from flask import current_app

def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class UserProfile:
    def __init__(self, id=None, name=None, description=None, status=None):
        self.id = id
        self.name = name
        self.description = description
        self.status = status

    def getId(self):
        return self.id

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status
        }

    # By default all created profiles are active.
    def createProfile(self):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_profile (name, description, status) VALUES (?, ?, ?)", (self.name, self.description, self.status))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user profile: {str(e)}")
            return False
        

    def updateProfile(self):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("UPDATE user_profile SET name = ?, description = ?, status = ? WHERE id = ?", (self.name, self.description, self.status, self.id))
            conn.commit()
            conn.close()    
            return True
        except Exception as e:
            print(f"Error updating user profile: {str(e)}")
            return False

    @staticmethod
    def isNameTaken(name):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_profile WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        
        if result == None:
            return False
        else:
            return True 
    @staticmethod
    def getAllProfiles():
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, status FROM user_profile")
            rows = cursor.fetchall()
            conn.close()
            profiles = []
            for row in rows:
                profiles.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'status': row[3]
                })
            return profiles
        except Exception as e:
            print(f"[ERROR] Error retrieving user profiles: {str(e)}")
            return None
    @staticmethod
    def getProfileById(profileId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, status FROM user_profile WHERE id = ?", (profileId,))
            result = cursor.fetchone()
            conn.close()
            if result:
                    userProfile = UserProfile(id=result[0], name=result[1], description=result[2], status=result[3])
                    return userProfile
            else:
                    return None
        except Exception as e:
            print(f"[ERROR] Error retrieving user profile by ID: {str(e)}")
            return None
    @staticmethod
    def searchProfiles(profileId=None, name=None):
        try:
            conn = getDb()
            cursor = conn.cursor()

            query = "SELECT id, name, description, status FROM user_profile WHERE 1=1"
            params = []

            if profileId is not None:
                query += " AND id = ?"
                params.append(profileId)

            if name:
                query += " AND name LIKE ?"
                params.append(f"%{name}%")

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            profiles = []
            for row in results:
                profile = UserProfile(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    status=row[3]
                )
                profiles.append(profile)

            return profiles

        except Exception as e:
            print(f"Error filtering profiles: {str(e)}")
            return []

    
