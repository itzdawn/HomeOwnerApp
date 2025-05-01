import sqlite3
import random
from datetime import datetime
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
       
def insertService(cleanerId, categoryId, name, description, price, shortlists, views, creationDate):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service (cleaner_id, category_id, name, description, price, shortlists, views, creation_date) VALUES (?,?,?,?,?,?,?,?)", 
                   (cleanerId, categoryId, name, description, price, shortlists, views, creationDate))
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
        print(f"CleanerID: [{service[1]}], Name: [{service[2]}], Category: [{service[4]}], Shortlists: [{service[6]}], Views: [{service[7]}]")
        count += 1
    print(f"Total Services: {count}")
    conn.close()

def createFakeServices(ENTRIES):
    conn = getDb()
    cursor = conn.cursor()
    
    #getting all cleaner id
    cursor.execute("SELECT id FROM user WHERE role = 'Cleaner'")
    cleanerIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM service_category")
    result = cursor.fetchall()
    categoryDict = {row[0]: row[1] for row in result}
    
    for x in range(ENTRIES):
        cleanerId = random.choice(cleanerIds)
        randomCategory = random.choice(list(categoryDict.items()))
        categoryId = randomCategory[0]
        name = randomCategory[1] + " Cleaning"
        description = name + "-" + str(datetime.now().strftime("%d-%m-%Y"))
        price = random.randint(25,125)
        shortlists = 0
        views = random.randint(0,70)
        creationDate = datetime.now().strftime("%d-%m-%Y")
        insertService(cleanerId,categoryId,name,description,price,shortlists,views,creationDate)
    
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    # dropServiceTable()
    # createServiceTables()
    # createFakeServices(ENTRIES)
    viewTable()