import sqlite3
from datetime import datetime

DATABASE = 'data/app.db'

class Service:
    def __init__(self, id=None, userId=None, name=None, description=None, category=None, price=None, shortlists=None, views=None, creationDate=None):
        self.__id = id
        self.__userId = userId
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.shortlists = shortlists
        self.views = views
        self.creationDate = creationDate if creationDate else datetime.now()
    
    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__userId
    
    #insert to database.
    def save(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO service (cleaner_id, name, description, category, price, shortlists, views, creation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.getUserId, self.name, self.description, self.category, self.price, self.shortlists, self.views, self.creationDate))
        conn.commit()
        conn.close()
    
    #retrieve service info by cleanerId from db
    @staticmethod
    def getServiceByUser(userId):
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE cleaner_id = ?", (userId,))
        results = cursor.fetchall() #list of service tuples
        conn.close()
        
        services = []
        for result in results:
            services.append(Service(
                id=result[0],
                userId=result[1],
                name=result[2],
                description=result[3],
                category=result[4],
                price=result[5],
                shortlists=result[6],
                views=result[7],
                creationDate=result[8]
            ))
        return services
    
    #retrieve service info by service id from db
    @staticmethod
    def getServiceByUser(serviceId):
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (serviceId,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return Service(
                id=result[0],
                userId=result[1],
                name=result[2],
                description=result[3],
                category=result[4],
                price=result[5],
                shortlists=result[6],
                views=result[7],
                creationDate=result[8]
            )
        else:
            return None