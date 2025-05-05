import sqlite3
from datetime import datetime
from flask import current_app


def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

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
        self.creationDate = creationDate if creationDate else datetime.now().strftime("%d-%m-%Y")
    
    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__userId
    
    # Convert service object to dictionary for JSON serialization
    def to_dict(self):
        """
        Convert Service object to dictionary for JSON serialization
        """
        return {
            'id': self.__id,
            'userId': self.__userId,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'shortlists': self.shortlists,
            'views': self.views,
            'creationDate': self.creationDate
        }
    
    #insert to database.
    def createService(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO service (cleaner_id, name, description, category, price, shortlists, views, creation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.getUserId, self.name, self.description, self.category, self.price, self.shortlists, self.views, self.creationDate))
        conn.commit()
        conn.close()
    
    def updateService(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE service
            SET name = ?, description = ?, category = ?, price = ?
            WHERE id = ? AND cleaner_id = ?
        """, (self.name, self.description, self.category, self.price, self.__id, self.__userId))
        conn.commit()
        conn.close()
    
    #retrieve service info by cleanerId from db, return type: list of service objects
    @staticmethod
    def getServiceByUserId(userId):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service WHERE cleaner_id = ?", (userId,))
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
    def getServiceByServiceId(serviceId):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service WHERE id = ?", (serviceId,))
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
    
    @staticmethod
    def deleteService(serviceId, userId):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM service WHERE id = ? AND cleaner_id = ?", (serviceId, userId))
        conn.commit()
        conn.close()
    
    #return list of tuples
    @staticmethod
    def searchServices(keyword):
        conn = getDb()
        cursor = conn.cursor()
        wildcard = f'%{keyword}%'
        cursor.execute("""
            SELECT * FROM service
            WHERE name LIKE ? OR description LIKE ?
        """, (wildcard, wildcard))
        results = cursor.fetchall()
        conn.close()
        return results
        
    # Service Category related methods
    @staticmethod
    def create_category(name, description=""):
        """
        Create a new service category
        
        Args:
            name (str): Category name
            description (str, optional): Category description
            
        Returns:
            int: ID of the created category, or None if failed
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO service_category (name, description)
                VALUES (?, ?)
            """, (name, description))
            category_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return category_id
        except Exception as e:
            print(f"Error creating category: {e}")
            return None
    
    @staticmethod
    def update_category(category_id, name, description=""):
        """
        Update an existing service category
        
        Args:
            category_id (int): ID of category to update
            name (str): New category name
            description (str, optional): New category description
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE service_category
                SET name = ?, description = ?
                WHERE id = ?
            """, (name, description, category_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    @staticmethod
    def delete_category(category_id):
        """
        Delete a service category
        
        Args:
            category_id (int): ID of category to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            # Check if category is in use by any services
            cursor.execute("SELECT COUNT(*) FROM service WHERE category = ?", (category_id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Category is in use, cannot delete
                conn.close()
                return False
            
            # Delete category
            cursor.execute("DELETE FROM service_category WHERE id = ?", (category_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Get a service category by ID
        
        Args:
            category_id (int): ID of category to retrieve
            
        Returns:
            dict: Category data, or None if not found
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sc.*, COUNT(s.id) as service_count
                FROM service_category sc
                LEFT JOIN service s ON sc.id = s.category
                WHERE sc.id = ?
                GROUP BY sc.id
            """, (category_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return dict(result)
            return None
        except Exception as e:
            print(f"Error getting category: {e}")
            return None
    
    @staticmethod
    def get_all_categories():
        """
        Get all service categories
        
        Returns:
            list: List of category dictionaries
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sc.*, COUNT(s.id) as service_count
                FROM service_category sc
                LEFT JOIN service s ON sc.id = s.category
                GROUP BY sc.id
                ORDER BY sc.name
            """)
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    @staticmethod
    def search_categories(keyword):
        """
        Search for service categories by name or description
        
        Args:
            keyword (str): Search term
            
        Returns:
            list: List of matching category dictionaries
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            wildcard = f"%{keyword}%"
            cursor.execute("""
                SELECT sc.*, COUNT(s.id) as service_count
                FROM service_category sc
                LEFT JOIN service s ON sc.id = s.category
                WHERE sc.name LIKE ? OR sc.description LIKE ?
                GROUP BY sc.id
                ORDER BY sc.name
            """, (wildcard, wildcard))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error searching categories: {e}")
            return []
        
    @staticmethod
    def filterServices(userId=None, serviceId=None, serviceName=None, category=None):
        """
        Advanced method to filter services with multiple criteria
        
        Args:
            userId (int, optional): Filter by user ID
            serviceId (int, optional): Filter by service ID
            serviceName (str, optional): Filter by service name (partial match)
            category (str, optional): Filter by category
            
        Returns:
            list: List of Service objects matching criteria
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            
            # Build query dynamically based on provided filters
            query = "SELECT * FROM service WHERE 1=1"
            params = []
            
            if userId:
                query += " AND cleaner_id = ?"
                params.append(userId)
                
            if serviceId:
                query += " AND id = ?"
                params.append(serviceId)
                
            if serviceName:
                query += " AND name LIKE ?"
                params.append(f"%{serviceName}%")
                
            if category:
                query += " AND category = ?"
                params.append(category)
                
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            conn.close()
            
            # Convert to Service objects
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
            
        except Exception as e:
            print(f"Error filtering services: {e}")
            return []
