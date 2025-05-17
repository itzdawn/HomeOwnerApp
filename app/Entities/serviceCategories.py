import sqlite3
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
    
    def toDict(self):
        return {
            'id': self.getId(),
            'name': self.name,
            'description': self.description
        }
    def createCategory(self):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO service_category (name, description) VALUES (?,?)", (self.name, self.description))
            conn.commit()
            if cursor.rowcount == 0:
                conn.close()
                return {"message": f"Unable to create service category: {self.name}", "success": False}
            conn.close()
            return {"message": f"Service Category: {self.name} created successfully", "success": True}
            
        except Exception as e:
            print(f"Error creating service category: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}

    def updateCategory(self, name=None, description=None):
        try:
            name = name or self.name
            description = description or self.description
            
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE service_category 
                SET name = ?, description = ?
                WHERE id = ?
            """, (name, description, self.getId()))
            conn.commit()
            
            if cursor.rowcount == 0:
                conn.close()
                return {"success": False, "message": "Failed to update category"}
            conn.close()
            return {"success": True, "message": "Category updated successfully"}
        except Exception as e:
            print(f"Error updating service category: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
     
    @staticmethod   
    def getCategoryById(categoryId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""SELECT id, name, description
                        FROM service_category
                        WHERE id = ?""", (categoryId,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                category = ServiceCategory(id=result[0], name=result[1], description=result[2])
                return category
            else:
                return None
        except Exception as e:
            print(f"[ERROR] Error retrieving category by ID: {str(e)}")
            return None
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
    
    @staticmethod
    def getAllCategories():
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description FROM service_category")
            results = cursor.fetchall()
            conn.close()
            categoryList = []
            for result in results:
                category = ServiceCategory(
                    id=result[0],
                    name=result[1],
                    description=result[2]
                )
                categoryList.append(category)
            return categoryList
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return [] 

    @staticmethod
    def searchServiceCategories(name=None, categoryId=None):
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            query = """
                SELECT id, name, description
                FROM service_category
                WHERE 1=1
            """
            params = []

            if categoryId:
                query += " AND id = ?"
                params.append(categoryId)
            
            if name:
                query += " AND name LIKE ?"
                params.append(f"%{name}%")  

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            conn.close()

            categories = []
            for result in results:
                category = ServiceCategory(
                    id=result[0],
                    name=result[1],
                    description=result[2]
                )
                categories.append(category)
            return categories
        except Exception as e:
            print(f"Error filtering service categories: {e}")
            return []
    
    @staticmethod
    def deleteCategory(categoryId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM service_category WHERE id = ?", (categoryId,))
            rowcount = cursor.rowcount
            conn.commit()
            if rowcount > 0:
                conn.close()
                return {"success": True, "message": "Service Category deleted successfully"} 
            conn.close()
            return {"success": False, "message": "Failed to delete service category"}
        except Exception as e:
            print(f"Error in delete category: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
    