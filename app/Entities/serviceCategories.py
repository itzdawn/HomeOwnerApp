import sqlite3
from datetime import datetime
from flask import current_app

def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn


class ServiceCategory:
    def __init__(self, id=None, name=None, description=None):
        self.__id = id
        self.name = name
        self.description = description
        
    def getId(self):
        return self.__id
    
    #used for cleaner during service creation.
    @staticmethod
    def getCategoryNames():
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM service_category")
            results = cursor.fetchall()
            conn.close()
            categoryList = []
            for result in results:
                categoryList.append({'id': result[0], 'name': result[1]})
            return categoryList
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []
        