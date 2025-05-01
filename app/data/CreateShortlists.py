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

def createShortlistTables():
    conn = getDb()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS shortlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        homeowner_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        shortlist_date TEXT NOT NULL,
        FOREIGN KEY (homeowner_id) REFERENCES user(id),
        FOREIGN KEY (service_id) REFERENCES service(id),
        UNIQUE(homeowner_id, service_id)
    );""")
    
    conn.commit()
    conn.close()

#DELETE THE ENTIRE TABLE AND SET SHORTLISTS ALL BACK TO 0
def dropTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('UPDATE service SET shortlists = 0')
    print("Service shortlists count reset to 0.")
    cursor.execute('DROP TABLE IF EXISTS shortlist')
    conn.commit()
    print("Shortlist table dropped.")
    conn.close()

def insertShortlist(homeownerId, serviceId, creationDate):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shortlist (homeowner_id, service_id, shortlist_date) VALUES (?,?,?)", 
                   (homeownerId, serviceId, creationDate))
    conn.commit()
    conn.close()

def viewTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shortlist') #list of tuples
    shortlists = cursor.fetchall()
    print(shortlists)
    conn.close()

#update the service's shortlist count
def updateShortlistCount(serviceId):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("SELECT id from service WHERE id = ?", (serviceId,))
    service = cursor.fetchone()
    if service:
        cursor.execute("""UPDATE service SET shortlists = shortlists + 1 WHERE id = ?""", (serviceId,))
        conn.commit()
        print(f"Shortlist count updated for service ID {serviceId}")
    else:
        print(f"Service ID {serviceId} not found.")  
    
         
def createFakeShortlists(ENTRIES):
    conn = getDb()
    cursor = conn.cursor()
    
    #getting all ids
    cursor.execute("SELECT id FROM user WHERE role = 'HomeOwner'")
    homeownerIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM service")
    serviceIds = [row[0] for row in cursor.fetchall()]
    
    for x in range(ENTRIES):
        homeownerId = random.choice(homeownerIds)
        serviceId = random.choice(serviceIds)
        creationDate = datetime.now().strftime("%d-%m-%Y")
        cursor.execute("""
            SELECT 1 FROM shortlist WHERE homeowner_id = ? AND service_id = ?
        """, (homeownerId, serviceId))
        exists = cursor.fetchone()
        if not exists:
            insertShortlist(homeownerId, serviceId, creationDate)
            updateShortlistCount(serviceId)
        else:
            print("Duplicate combination.")
        
    
if __name__ == '__main__':
    # dropTable()
    # createShortlistTables()
    # createFakeShortlists(ENTRIES)
    viewTable()
