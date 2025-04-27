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
            INSERT INTO services (id, userId, name, description, category, price, shortlists, views, creationDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.getId, self.getUserId, self.name, self.description, self.price, self.category, self.views, self.shortlists, self.creationDate))
        conn.commit()
        conn.close()