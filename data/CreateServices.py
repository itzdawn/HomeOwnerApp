import sqlite3
import random
from datetime import datetime

DATABASE = 'data/app.db'
ENTRIES = 100 #Number of entries generated.

#DB connection
def getDb():
    conn = sqlite3.connect(DATABASE)
    return conn

def createServiceTables():
    conn = getDb()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS service (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   
        cleaner_id INTEGER NOT NULL,             
        name TEXT NOT NULL,                      
        description TEXT,
        category TEXT,                      
        price REAL,
        shortlists INTEGER DEFAULT 0,                                                                      
        views INTEGER DEFAULT 0,                 
        creation_date TEXT NOT NULL,
        FOREIGN KEY (cleaner_id) REFERENCES user(id)                
        );""")
    
    conn.commit()
    conn.close()
    
#DELETE OUT THE ENTIRE TABLE.
def dropServiceTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS service')
    conn.commit()
    print("Service table dropped.")
    conn.close()
       
def insertService(cleanerId, name, description, category, price, shortlists, views, creationDate):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service (cleaner_id, name, description, category, price, shortlists, views, creation_date) VALUES (?,?,?,?,?,?,?,?)", 
                   (cleanerId, name, description, category, price, shortlists, views, creationDate))
    conn.commit()
    conn.close()

def viewTable():
    count = 0
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM service') #list of tuples
    services = cursor.fetchall()
    print("Services:")
    for service in services:
        print(f"CleanerID: [{service[1]}], Name: [{service[2]}], Category: [{service[4]}], Shortlists: [{service[6]}], Views: [{service[7]}]")
        count += 1
    print(f"Total Services: {count}")
    conn.close()

def createFakeServices(ENTRIES):
    conn = getDb()
    cursor = conn.cursor()
    
    #getting all userid that's a cleaner
    cursor.execute("SELECT id FROM user WHERE role = 'Cleaner'")
    cleanerIds = [row[0] for row in cursor.fetchall()]
    if not cleanerIds:
        return "No cleaners"
    
    for x in range(ENTRIES):
        categories = [
            "Bathroom",
            "Kitchen",
            "Bedroom",
            "Living Room",
            "Storage",
            "Laundry",
            "Windows",
            "Floors & Carpets"
        ]
        category = random.choice(categories)
        name = random.choice(categories) + " Cleaning"
        description = name + str(datetime.now())
        price = random.randint(25,125)
        shortlists = random.randint(0,30)
        views = random.randint(0,70)
        creationDate = datetime.now()
        cleanerId = random.choice(cleanerIds)
        insertService(cleanerId,name,description,category,price,shortlists,views,creationDate)
    
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    # dropServiceTable()
    # createServiceTables()
    # createFakeServices(ENTRIES)
    viewTable()