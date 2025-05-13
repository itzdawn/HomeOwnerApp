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
        self.categoryName = None
    
    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__userId
    
    # Convert service object to dictionary for JSON serialization
    def toDict(self):
        return {
            "id": self.getId(),
            "userId": self.getUserId(),
            "name": self.name,
            "description": self.description,
            "categoryId": self.categoryId,
            "price": self.price,
            "shortlists": self.shortlists,
            "views": self.views,
            "creationDate": self.creationDate,
            "categoryName": getattr(self, "categoryName", None),
        }

    #insert to database.
    def createService(self):
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO service (cleaner_id, category_id, name, description, price, shortlists, views, creation_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.getUserId(), self.categoryId, self.name, self.description, self.price, self.shortlists, self.views, self.creationDate))
            conn.commit()
            if cursor.rowcount == 0:
                conn.close()
                return {"message": f"Unable to create Service: {self.name}", "success": False}
            conn.close()
            return {"message": f"Service: {self.name} created successfully", "success": True}
        except Exception as e:
            print(f"[CreateServiceController] Error: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
        
    def updateService(self, name=None, description=None, price=None):
        try:
            #use existing values if parameters are not provided
            name = name or self.name
            description = description or self.description
            price = price if price is not None else self.price
            
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE service
                SET category_id = ?, name = ?, description = ?, price = ?
                WHERE id = ? AND cleaner_id = ?
            """, (self.categoryId, name, description, price, self.getId(), self.getUserId()))
            conn.commit()
            conn.close()
            if cursor.rowcount == 0:
                return {"success": False, "message": "Failed to update user"}
            return {"success": True, "message": "Service updated successfully"}
        except Exception as e:
            print(f"Error updating service: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    #retrieve service info by cleanerId from db, return type: list of service objects
    @staticmethod
    def getAllServiceByUserId(userId):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
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
                    id=result["id"],
                    userId=result["cleaner_id"],
                    name=result["name"],
                    description=result["description"],
                    categoryId=result["category_id"],
                    price=result["price"],
                    shortlists=result["shortlists"],
                    views=result["views"],
                    creationDate=result["creation_date"]
                )
                service.categoryName = result["category_name"]
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
            conn.row_factory = sqlite3.Row
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
                    id=result["id"],
                    userId=result["cleaner_id"],
                    name=result["name"],
                    description=result["description"],
                    categoryId=result["category_id"],
                    price=result["price"],
                    shortlists=result["shortlists"],
                    views=result["views"],
                    creationDate=result["creation_date"]
                )
                service.categoryName = result["category_name"]
                return service
            else:
                return None
        except Exception as e:
            print(f"Error getting service by ID: {e}")
            return None
    
    @staticmethod
    def getAllServices():
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
            """)
            results = cursor.fetchall()
            conn.close()
            
            services = []
            for result in results:
                service = Service(
                    id=result["id"],
                    userId=result["cleaner_id"],
                    name=result["name"],
                    description=result["description"],
                    categoryId=result["category_id"],
                    price=result["price"],
                    shortlists=result["shortlists"],
                    views=result["views"],
                    creationDate=result["creation_date"]
                )
                service.categoryName = result["category_name"]
                services.append(service)
            return services
        except Exception as e:
            print(f"Error retrieving all services: {e}")
            return []
            
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
            if rowcount > 0:
                return {"success": True, "message": "Service deleted successfully"}
            return {"success": False, "message": "Failed to delete service"}
        except Exception as e:
            print(f"Error in deleteService: {e}")
            return {"success": False, "message": f"Error: {str(e)}"}
    
    @staticmethod
    def searchServices(userId=None, serviceId=None, serviceName=None, categoryId=None):
        """
        Returns:
            list: List of Service objects matching criteria
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row 
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
                    id=result["id"],
                    userId=result["cleaner_id"],
                    name=result["name"],
                    description=result["description"],
                    categoryId=result["category_id"],
                    price=result["price"],
                    shortlists=result["shortlists"],
                    views=result["views"],
                    creationDate=result["creation_date"]
                )
                service.categoryName = result["category_name"]
                services.append(service)
            return services
            
        except Exception as e:
            print(f"Error filtering services: {e}")
            return []

    @staticmethod
    def searchAvailServices(serviceName=None, categoryId=None):
        """
        Returns:
            list: List of Service objects matching category ID or service name
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            query = """
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.is_deleted = 0
            """
            params = []

            if categoryId:
                query += " AND s.category_id = ?"
                params.append(categoryId)

            if serviceName:
                query += " AND s.name LIKE ?"
                params.append(f"%{serviceName}%")

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            conn.close()

            services = []
            for result in results:
                service = Service(
                    id=result["id"],
                    userId=result["cleaner_id"],
                    name=result["name"],
                    description=result["description"],
                    categoryId=result["category_id"],
                    price=result["price"],
                    shortlists=result["shortlists"],
                    views=result["views"],
                    creationDate=result["creation_date"]
                )
                service.categoryName = result["category_name"]
                services.append(service)
            return services

        except Exception as e:
            print(f"Error filtering services: {e}")
            return []

    @staticmethod
    def getAvailServiceByServiceId(serviceId):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.*, sc.name AS category_name, u.username AS cleaner_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                LEFT JOIN user u ON s.cleaner_id = u.id
                WHERE s.id = ? AND s.is_deleted = 0
            """, (serviceId,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    "id": result["id"],
                    "name": result["name"],
                    "description": result["description"],
                    "categoryId": result["category_id"],
                    "categoryName": result["category_name"],
                    "price": result["price"],
                    "shortlists": result["shortlists"],
                    "views": result["views"],
                    "creationDate": result["creation_date"],
                    "cleanerId": result["cleaner_id"],
                    "cleanerName": result["cleaner_name"]
                }
            else:
                return None

        except Exception as e:
            print(f"Error in getAvailServicesByServiceId: {e}")
            return None