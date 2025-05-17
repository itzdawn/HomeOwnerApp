"""
This file uses faker library to generate fake info and populate app.db
"""

import sqlite3
from faker import Faker
import random
import os

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE= os.path.join(baseDir, 'data', 'app.db')
fake = Faker("en_MS") #Basically malaysian locale because there's no sg.
ENTRIES = 100 #Number of fake entries generated

#DB connection
def getDb():
    conn = sqlite3.connect(DATABASE)
    return conn

def createUserTables():
    conn = getDb()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        profile_id INTEGER NOT NULL,
        status INTEGER,
        FOREIGN KEY (profile_id) REFERENCES user_profile(id)
    )""")
    
    conn.commit()
    conn.close()

def insertUsers(username, password, profileId, status):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (username, password, profile_id, status) VALUES (?,?,?,?)", (username, password, profileId, status))
    conn.commit()
    conn.close()

def isUsernameUsed(username):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result == None:
            return False
        else:
            return True
        
def generateUniqueUsername():
    while True:
        username = fake.user_name()
        if not isUsernameUsed(username):
            return username 
        
def generateAndInsert(ENTRIES):
    createUserTables()
    
    for x in range(ENTRIES):
        n = random.randint(7, 12) #random password length between 7 to 12.
        username = generateUniqueUsername()
        password = fake.password(length=n)
        profileId = random.randint(1,4) #assuming only 4 default ids
        status = 1 #all accounts are active
        
        insertUsers(username,password,profileId,status)

#DELETE OUT THE ENTIRE TABLE.
def dropUserTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user')
    conn.commit()
    print("User table dropped.")
    conn.close()

def viewTable():
    count = 0
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user.username, user.password, user.status, user_profile.name
        FROM user
        JOIN user_profile ON user.profile_id = user_profile.id
    ''')
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        status = "Active" if user[2] == 1 else "Inactive"
        print(f"Username: [{user[0]}], Password: [{user[1]}], Profile: [{user[3]}] Status: [{status}]")
        count += 1
    print(f"Total Users: {count}")
    conn.close()
    
def run():
    dropUserTable()
    generateAndInsert(ENTRIES)
    viewTable()
        
if __name__ == '__main__':
    # dropUserTable()
    # generateAndInsert(ENTRIES)
    viewTable()    