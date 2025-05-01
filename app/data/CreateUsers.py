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
        role TEXT NOT NULL,
        status INTEGER
    )""")
    
    conn.commit()
    conn.close()

def insertUsers(username, password, role, status):
    conn = getDb()
    cursor = conn.cursor()
    #apparently for sqlite, ? is the placeholder
    cursor.execute("INSERT INTO user (username, password, role, status) VALUES (?,?,?,?)", (username, password, role, status))
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
    roles = ["Admin", "HomeOwner", "Cleaner", "PlatformManagement"]
    createUserTables()
    
    for x in range(ENTRIES):
        n = random.randint(7, 12) #random password length between 7 to 12.
        username = generateUniqueUsername()
        password = fake.password(length=n)
        role = roles[random.randint(0,3)]
        status = 1
        
        insertUsers(username,password,role,status)

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
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        status = "Active" if user[4] == 1 else "Inactive"
        print(f"Username: [{user[1]}], Password: [{user[2]}], Role: [{user[3]}] Status: [{status}]")
        count += 1
    print(f"Total Users: {count}")
    conn.close()
    
         
if __name__ == '__main__':
    # dropUserTable()
    # generateAndInsert(ENTRIES)
    viewTable()    