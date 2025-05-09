import sqlite3
from datetime import datetime
from flask import current_app


def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class Service:
    def __init__(self, id=None, userId=None, name=None, description=None, categoryId=None, price=None, shortlists=None, views=None, creationDate=None):
        self.__id = id
        self.__userId = userId
        self.name = name
        self.description = description
        self.categoryId = categoryId
        self.price = price
        self.shortlists = shortlists
        self.views = views
        self.creationDate = creationDate if creationDate else datetime.now().strftime("%d-%m-%Y")
        self.category_name = None
    
    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__userId
    
    # Convert service object to dictionary for JSON serialization
    def toDict(self):
        # Check if category_name was already populated from JOIN query
        category_name = getattr(self, 'category_name', None)
        
        # If category_name is not yet set but we have a category ID, fetch it
        categoryId = self.categoryId
        if category_name is None and categoryId is not None:
            try:
                conn = getDb()
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM service_category WHERE id = ?", (categoryId,))
                result = cursor.fetchone()
                conn.close()
                if result:
                    category_name = result[0]
                    # Store for future use
                    self.category_name = category_name
            except Exception as e:
                print(f"Error getting category name: {e}")
        
        # Fix potential data type issues
        if not isinstance(categoryId, int) and categoryId is not None:
            try:
                categoryId = int(categoryId)
            except (ValueError, TypeError):
                # If conversion fails, keep original value
                pass
        
        service_dict = {
            'id': self.getId(),
            'cleaner_id': self.getUserId(),
            'name': self.name,
            'description': self.description,
            'category_id': categoryId,
            'category_name': category_name,  # Include category_name
            'price': self.price,
            'shortlists': self.shortlists,
            'views': self.views,
            'creation_date': self.creationDate
        }
        return service_dict
    
    #insert to database.
    def createService(self):
        conn = getDb()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO service (cleaner_id, category_id, name, description, price, shortlists, views, creation_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.getUserId(), self.categoryId, self.name, self.description, self.price, self.shortlists, self.views, self.creationDate))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating service: {e}")
            return False
        
    def updateService(self):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE service
                SET category_id = ?, name = ?, description = ?, price = ?
                WHERE id = ? AND cleaner_id = ?
            """, (self.categoryId, self.name, self.description, self.price, self.getId(), self.getUserId()))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating service: {e}")
            return False
    
    #retrieve service info by cleanerId from db, return type: list of service objects
    @staticmethod
    def getAllServiceByUserId(userId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.cleaner_id = ? AND s.is_deleted = 0
            """, (userId,))
            results = cursor.fetchall() #list of service tuples
            conn.close()
            
            services = []
            for result in results:
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    categoryId=result[2],
                    price=result[5],
                    shortlists=result[6],
                    views=result[7],
                    creationDate=result[8]
                )
                # Store category_name if it exists in the result
                if len(result) > 9:
                    service.category_name = result[9]
                    print(f"DEBUG - Service {result[0]} has category_name: {result[9]}")
                services.append(service)
            return services
        except Exception as e:
            print(f"Error getting services by user ID: {e}")
            return []
    
    #retrieve service info by service id from db
    @staticmethod
    def getServiceByServiceId(serviceId):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.id = ? AND s.is_deleted = 0
            """, (serviceId,))
            result = cursor.fetchone()
            conn.close()
            if result:
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    categoryId=result[2],
                    price=result[5],
                    shortlists=result[6],
                    views=result[7],
                    creationDate=result[8]
                )
                # Store category_name if it exists in the result
                if len(result) > 9:
                    service.category_name = result[9]
                return service
            else:
                print(f"DEBUG - Service {serviceId} not found")
                return None
        except Exception as e:
            print(f"Error getting service by ID: {e}")
            return None
        
    @staticmethod
    def deleteService(serviceId, userId):
        """
        Soft-delete a service by setting service.is_deleted = 1
        Returns:
            bool: True if service was marked as deleted, False otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE service SET is_deleted = 1 WHERE id = ? AND cleaner_id = ? AND is_deleted = 0",
                (serviceId, userId)
            )
            rowcount = cursor.rowcount
            conn.commit()
            conn.close()
            return rowcount > 0 #return true is >0 rows are affected.
        except Exception as e:
            print(f"Error in deleteService: {e}")
            return False
    
    @staticmethod
    def searchServices(userId=None, serviceId=None, serviceName=None, categoryId=None):
        """
        Returns:
            list: List of Service objects matching criteria
        """
        try:
            conn = getDb()
            cursor = conn.cursor()

            query = """
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.is_deleted = 0
            """
            params = []
            
            if userId:
                query += " AND s.cleaner_id = ?"
                params.append(userId)
                
            if serviceId:
                query += " AND s.id = ?"
                params.append(serviceId)
                
            if serviceName:
                query += " AND s.name LIKE ?"
                params.append(f"%{serviceName}%")
                
            if categoryId:
                query += " AND s.category_id = ?"
                params.append(categoryId)
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            conn.close()
            
            services = []
            for result in results:
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    categoryId=result[2],
                    price=result[5],
                    shortlists=result[6],
                    views=result[7],
                    creationDate=result[8]
                )
                if len(result) > 9:
                    service.category_name = result[9]
                services.append(service)
            return services
            
        except Exception as e:
            print(f"Error filtering services: {e}")
            return []

