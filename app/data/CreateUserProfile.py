import sqlite3
import os

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE= os.path.join(baseDir, 'data', 'app.db')

defaultProfiles = {
    "Admin": "Full system access and user management privileges.",
    "HomeOwner": "Property owner with access to manage bookings and listings.",
    "Cleaner": "Assigned to maintain and clean properties as scheduled.",
    "PlatformManagement": "Oversees platform operations and content moderation."
    }

#DB connection
def getDb():
    conn = sqlite3.connect(DATABASE)
    return conn

def createTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status INTEGER
        )
        ''')    
    conn.commit()
    conn.close()

def populateTable(profiles):
    conn = getDb()
    cursor = conn.cursor()
    status = 1
    for name, description in profiles.items():
        cursor.execute("""
            INSERT INTO user_profile (name, description, status)
            VALUES (?,?,?)""", (name, description, status))
    conn.commit()
    conn.close()
    
def dropUserTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user_profile')
    conn.commit()
    print("User table dropped.")
    conn.close()
    
def viewTable():
    count = 0
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profile')
    userProfiles = cursor.fetchall()
    print("User Profiles:")
    for profile in userProfiles:
        print(f"Profile: [{profile[1]}], Description: [{profile[2]}], Status: {profile[3]}")
        count+=1
    print(f"Total Profiles: {count}")
    conn.close()
    
def run():
    defaultProfiles = {
    "Admin": "Full system access and user management privileges.",
    "HomeOwner": "Property owner with access to manage bookings and listings.",
    "Cleaner": "Assigned to maintain and clean properties as scheduled.",
    "PlatformManagement": "Oversees platform operations and content moderation."
    }
    dropUserTable()
    createTable()
    populateTable(defaultProfiles) 
    viewTable()
if __name__ == "__main__":
    dropUserTable()
    createTable()
    populateTable(defaultProfiles) 
    viewTable()