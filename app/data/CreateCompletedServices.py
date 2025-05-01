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

def createCompletedServiceTable():
    conn = getDb()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS completed_service (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cleaner_id INTEGER NOT NULL,
        homeowner_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        service_date TEXT NOT NULL,
        FOREIGN KEY (cleaner_id) REFERENCES user(id),
        FOREIGN KEY (homeowner_id) REFERENCES user(id),
        FOREIGN KEY (service_id) REFERENCES service(id)
    );""")
    
    conn.commit()
    conn.close()

#DELETE THE ENTIRE TABLE
def dropTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS completed_service')
    conn.commit()
    print("Completed_Services table dropped.")
    conn.close()

def insertCompletedService(cleanerId, homeownerId, serviceId, serviceDate):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO completed_service (cleaner_id, homeowner_id, service_id, service_date) VALUES (?,?,?,?)", 
                   (cleanerId, homeownerId, serviceId, serviceDate))
    conn.commit()
    conn.close()

def viewTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM completed_service') #list of tuples
    completedServices = cursor.fetchall()
    print(completedServices)
    conn.close()

def createFakeCompletedServices(ENTRIES):
    conn = getDb()
    cursor = conn.cursor()
    
    #getting all ids
    cursor.execute("SELECT id FROM user WHERE role = 'Cleaner'")
    cleanerIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM user WHERE role = 'HomeOwner'")
    homeownerIds = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM service")
    serviceIds = [row[0] for row in cursor.fetchall()]
    
    for x in range(ENTRIES):
        randomDays = random.randint(1,30)
        cleanerId = random.choice(cleanerIds)
        homeownerId = random.choice(homeownerIds)
        serviceId = random.choice(serviceIds)
        cursor.execute("SELECT creation_date FROM service WHERE id = ?", (serviceId,))
        result = cursor.fetchone()
        creationDate = result[0]
        serviceDateObj = datetime.strptime(creationDate, "%d-%m-%Y") + timedelta(days=randomDays)
        serviceDate = serviceDateObj.strftime("%d-%m-%Y")
        insertCompletedService(cleanerId,homeownerId,serviceId,serviceDate) 
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    dropTable()
    createCompletedServiceTable()
    createFakeCompletedServices(ENTRIES)
    viewTable()

