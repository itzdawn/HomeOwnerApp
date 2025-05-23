import sqlite3
import random
from datetime import datetime, timedelta
import os

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE= os.path.join(baseDir, 'data', 'app.db')
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
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        shortlists INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0,
        creation_date TEXT NOT NULL,
        is_deleted INTEGER DEFAULT 0,
        FOREIGN KEY (cleaner_id) REFERENCES user(id),
        FOREIGN KEY (category_id) REFERENCES service_category(id)
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
       
def insertService(cleanerId, category_id, name, description, price, shortlists, views, creationDate):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service (cleaner_id, category_id, name, description, price, shortlists, views, creation_date) VALUES (?,?,?,?,?,?,?,?)", 
                   (cleanerId, category_id, name, description, price, shortlists, views, creationDate))
    conn.commit()
    conn.close()

def viewTable():
    count = 0
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM service') #list of tuples
    services = cursor.fetchall()
    # print(services)
    print("Services:")
    for service in services:
        print(f"CleanerID: [{service[1]}], Name: [{service[3]}], Category: [{service[4]}], Shortlists: [{service[6]}], Views: [{service[7]}]")
        count += 1
    print(f"Total Services: {count}")
    conn.close()

def createFakeServices(ENTRIES):
    conn = getDb()
    cursor = conn.cursor()
    
    #getting all cleaner id
    cursor.execute("SELECT user.id FROM user JOIN user_profile ON user.profile_id = user_profile.id WHERE user_profile.name = 'Cleaner'")
    cleanerIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id, name, description FROM service_category")
    result = cursor.fetchall()
    categoryDict = {
        row[0]: {
            "name": row[1],
            "description": row[2]
        }
        for row in result
    }
    
    for x in range(ENTRIES):
        cleanerId = random.choice(cleanerIds)
        randomCategory = random.choice(list(categoryDict.items()))
        category_id = randomCategory[0]
        name = randomCategory[1]['name']
        description = randomCategory[1]["description"]
        price = random.randint(15,125)
        shortlists = 0
        views = random.randint(0,70)
        start_date = datetime(2025, 4, 1)
        end_date = datetime.now()
        random_days = random.randint(0, (end_date - start_date).days)
        creationDate = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        insertService(cleanerId,category_id,name,description,price,shortlists,views,creationDate)
    
    conn.commit()
    conn.close()
def run():
    dropServiceTable()
    createServiceTables()
    createFakeServices(ENTRIES)
    viewTable()
if __name__ == '__main__':
    dropServiceTable()
    createServiceTables()
    createFakeServices(ENTRIES)
    viewTable()