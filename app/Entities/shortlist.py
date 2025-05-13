import sqlite3
from flask import current_app
from datetime import datetime
from app.Entities.service import Service

def getDb():
    return sqlite3.connect(current_app.config['DATABASE'])

class Shortlist:
    def __init__(self, id=None, homeOwnerId=None, serviceId=None, shortlistDate=None):
        self.__id = id
        self.__homeOwnerId = homeOwnerId
        self.__serviceId = serviceId
        self.shortlistDate = shortlistDate if shortlistDate else datetime.now().strftime("%d-%m-%Y")
        
    def getId(self):
        return self.__id
    def getHomeOwnerId(self):
        return self.__homeOwnerId
    def getServiceId(self):
        return self.__serviceId

    @staticmethod
    def searchShortlistedServices(homeownerId, serviceName=None, categoryId=None):
        """Search for shortlisted services with details for a homeowner."""
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()

            query = """
                SELECT s.*, sl.shortlist_date, sc.name AS category_name
                FROM shortlist sl
                JOIN service s ON sl.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE sl.homeowner_id = ? AND s.is_deleted = 0
            """
            params = [homeownerId]

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
            for row in results:
                serviceDict = {
                    "id": row["id"],
                    "userId": row["cleaner_id"],
                    "name": row["name"],
                    "description": row["description"],
                    "categoryId": row["category_id"],
                    "categoryName": row["category_name"],
                    "price": row["price"],
                    "shortlists": row["shortlists"],
                    "views": row["views"],
                    "creationDate": row["creation_date"],
                    "shortlistDate": row["shortlist_date"]
                }
                services.append(serviceDict)

            return services

        except Exception as e:
            print(f"Error filtering shortlisted services: {e}")
            return []
        
    @staticmethod
    def getShortlists(homeownerId):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT s.*, sl.shortlist_date, sc.name AS category_name
                FROM shortlist sl
                JOIN service s ON sl.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE sl.homeowner_id = ? AND s.is_deleted = 0
            """, (homeownerId,))

            results = cursor.fetchall()
            conn.close()

            services = []
            for row in results:
                serviceDict = {
                    "id": row["id"],
                    "userId": row["cleaner_id"],
                    "name": row["name"],
                    "description": row["description"],
                    "categoryId": row["category_id"],
                    "categoryName": row["category_name"],
                    "price": row["price"],
                    "shortlists": row["shortlists"],
                    "views": row["views"],
                    "creationDate": row["creation_date"],
                    "shortlistDate": row["shortlist_date"]
                }
                services.append(serviceDict)

            return services

        except Exception as e:
            print(f"Error getting shortlisted services: {e}")
            return []
    
    @staticmethod
    def getShortlistedServiceDetail(serviceId, homeOwnerId):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT s.*, sc.name AS category_name, u.username AS cleaner_name, sh.shortlist_date
                FROM shortlist sh
                JOIN service s ON sh.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                LEFT JOIN user u ON s.cleaner_id = u.id
                WHERE sh.service_id = ? AND sh.homeowner_id = ?
            """, (serviceId, homeOwnerId))

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
                    "cleanerName": result["cleaner_name"],
                    "shortlistDate": result["shortlist_date"]
                }
            else:
                return None
        except Exception as e:
            print(f"[Shortlist.getShortlistedServiceDetail] Error: {e}")
            return None
        
    @staticmethod
    def addShortlist(homeOwnerId, serviceId):
        try:
            conn = getDb()
            cursor = conn.cursor()

            #Check if already shortlisted
            cursor.execute("""
                SELECT id FROM shortlist
                WHERE homeowner_id = ? AND service_id = ?
            """, (homeOwnerId, serviceId))

            if cursor.fetchone():
                conn.close()
                return {"success": False, "message": "Service already shortlisted."}

            # Insert into shortlist
            cursor.execute("""
                INSERT INTO shortlist (homeowner_id, service_id, shortlist_date)
                VALUES (?, ?, DATE('now'))
            """, (homeOwnerId, serviceId))
            insertCount = cursor.rowcount

            # Update counter
            cursor.execute("""
                UPDATE service SET shortlists = shortlists + 1
                WHERE id = ?
            """, (serviceId,))

            conn.commit()

            if insertCount == 0:
                conn.close()
                return {"success": False, "message": "Failed to shortlist the service."}
            conn.close()
            return {"success": True, "message": "Service shortlisted successfully!"}

        except Exception as e:
            print(f"[Shortlist.addShortlist] Error: {e}")
            return {"success": False, "message": "Unexpected error occurred"}

    #currently not in user story.    
    @staticmethod
    def removeShortlist(homeOwnerId, serviceId):
        try:
            conn = getDb()
            cursor = conn.cursor()

            #Delete from shortlist
            cursor.execute("""
                DELETE FROM shortlist
                WHERE homeowner_id = ? AND service_id = ?
            """, (homeOwnerId, serviceId))
            deleteCount = cursor.rowcount

            if deleteCount > 0:
                cursor.execute("""
                    UPDATE service
                    SET shortlists = CASE 
                        WHEN shortlists > 0 THEN shortlists - 1
                        ELSE 0
                    END
                    WHERE id = ?
                """, (serviceId,))
                conn.commit()
                conn.close()
                return {"success": True, "message": "Service removed from shortlist successfully!"}
            else:
                conn.close()
                return {"success": False, "message": "Service not found in shortlist or already removed."}

        except Exception as e:
            print(f"[Shortlist Entity] Error removing shortlist: {e}")
            return {"success": False, "message": "Unexpected error occurred"}