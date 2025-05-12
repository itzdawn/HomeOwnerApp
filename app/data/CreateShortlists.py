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
    
    # Get all HomeOwner IDs
    cursor.execute("""
        SELECT user.id FROM user 
        JOIN user_profile ON user.profile_id = user_profile.id 
        WHERE user_profile.name = 'HomeOwner'
    """)
    homeownerIds = [row[0] for row in cursor.fetchall()]

    # Get all service IDs and creation dates
    cursor.execute("SELECT id, creation_date FROM service")
    services = cursor.fetchall()
    serviceDict = {row[0]: datetime.strptime(row[1], "%Y-%m-%d") for row in services}

    inserted_count = 0
    max_attempts = ENTRIES * 10  
    attempts = 0

    while inserted_count < ENTRIES and attempts < max_attempts:
        homeownerId = random.choice(homeownerIds)
        serviceId = random.choice(list(serviceDict.keys()))
        serviceCreationDate = serviceDict[serviceId]
        now = datetime.now()

        if serviceCreationDate > now:
            attempts += 1
            continue  
        
        #generate a shortlist date between creation date and now
        total_days = (now - serviceCreationDate).days
        shortlist_date_obj = serviceCreationDate + timedelta(days=random.randint(0, total_days))
        shortlistDate = shortlist_date_obj.strftime("%d-%m-%Y")

        cursor.execute("""
            SELECT 1 FROM shortlist WHERE homeowner_id = ? AND service_id = ?
        """, (homeownerId, serviceId))
        exists = cursor.fetchone()

        if not exists:
            insertShortlist(homeownerId, serviceId, shortlistDate)
            updateShortlistCount(serviceId)
            inserted_count += 1
        else:
            print("Duplicate combination.")

        attempts += 1

    conn.commit()
    conn.close()


def run():
    dropTable()
    createShortlistTables()
    createFakeShortlists(ENTRIES)
    viewTable()
      
if __name__ == '__main__':
    dropTable()
    createShortlistTables()
    createFakeShortlists(ENTRIES)
    viewTable()
