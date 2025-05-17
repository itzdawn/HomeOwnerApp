import sqlite3
import os
import json

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE= os.path.join(baseDir, 'data', 'app.db')

#DB connection
def getDb():
    conn = sqlite3.connect(DATABASE)
    return conn

def createCategoryTable():
    conn = getDb()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS service_category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    );""")
        
    conn.commit()
    conn.close()

#DELETE THE ENTIRE TABLE
def dropTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS service_category')
    conn.commit()
    print("Table dropped.")
    conn.close()

def insertServiceCategory(name, description):
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service_category (name, description) VALUES (?,?)", 
                   (name, description))
    conn.commit()
    conn.close()

def viewTable():
    conn = getDb()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM service_category') #list of tuples
    completedServices = cursor.fetchall()
    print(completedServices)
    conn.close()

def createCategoriesFromJson(file):
    with open(file, 'r') as file:
        categories = json.load(file)

    for item in categories:
        category = item.get('category')
        description = item.get('description', '')
        if category:
            insertServiceCategory(category, description)
        else:
            print("Skipping invalid item:", item)

def run():
    dropTable()
    createCategoryTable()
    createCategoriesFromJson('app/data/service_categories.json')
    viewTable()
    
if __name__ == '__main__':
    file = 'app/data/service_categories.json'
    dropTable()
    createCategoryTable()
    createCategoriesFromJson(file)
    viewTable()

