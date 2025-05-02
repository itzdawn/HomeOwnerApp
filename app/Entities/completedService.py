import sqlite3
from datetime import datetime
from flask import current_app


def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class CompletedService:
    def __init__(self, id=None, cleanerId=None, homeOwnerId=None, serviceId=None, serviceDate=None):
        self.__id = id
        self.__cleanerId = cleanerId
        self.__homeOwnerId = homeOwnerId
        self.__serviceId = serviceId
        self.serviceDate = serviceDate if serviceDate else datetime.now().strftime("%d-%m-%Y")
    
    def getId(self):
        return self.__id
    def getHomeOwnerId(self):
        return self.__homeOwnerId
    def getCleanerId(self):
        return self.__cleanerId
    def getServiceId(self):
        return self.__serviceId
    
    def completeService(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO completed_service (cleaner_id, homeowner_id, service_id, service_date) VALUES (?,?,?,?)", 
                       (self.getCleanerId, self.getHomeOwnerId, self.getServiceId, self.serviceDate))
        conn.commit()
        conn.close()
    
    @staticmethod
    def searchPastServices(cleanerId, startDate=None, endDate=None, category=None):
        conn = getDb()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        query = """ SELECT cs.id AS CompletedServiceId, cs.cleaner_id, cs.homeowner_id, cs.service_id, cs.service_date,
            s.name, s.description, s.price, s.category, s.creation_date
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            WHERE cs.cleaner_id = ?
            """
        params = [cleanerId]
        if startDate:
            query += " AND cs.service_date >= ?"
            params.append(startDate)
        if endDate:
            query += " AND cs.service_date <= ?"
            params.append(endDate)
        if category:
            query += " AND s.category = ?"
            params.append(category)
            
        cursor.execute(query, tuple(params))
        queryResults = cursor.fetchall()
        conn.close()
        return [dict(result) for result in queryResults]



        
        
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # cleaner_id INTEGER NOT NULL,
    # homeowner_id INTEGER NOT NULL,
    # service_id INTEGER NOT NULL,
    # service_date TEXT NOT NULL,
    # FOREIGN KEY (cleaner_id) REFERENCES user(id),
    # FOREIGN KEY (homeowner_id) REFERENCES user(id),
    # FOREIGN KEY (service_id) REFERENCES service(id)