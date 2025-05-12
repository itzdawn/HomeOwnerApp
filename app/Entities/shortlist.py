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
    def add_to_shortlist(homeowner_id, service_id):
        """Add a service to the homeowner's shortlist and update counters."""
        conn = getDb()
        cursor = conn.cursor()
        try:
            # Insert into shortlist table
            cursor.execute(
                """INSERT INTO shortlist (homeowner_id, service_id, shortlist_date) 
                VALUES (?, ?, DATE('now'))""",
                (homeowner_id, service_id)
            )
            # Update service.shortlists counter
            cursor.execute(
                "UPDATE service SET shortlists = shortlists + 1 WHERE id = ?",
                (service_id,)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:  # Duplicate or invalid IDs
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def remove_from_shortlist(homeowner_id, service_id):
        """Remove a service from the homeowner's shortlist."""
        conn = getDb()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM shortlist WHERE homeowner_id = ? AND service_id = ?",
                (homeowner_id, service_id)
            )
            # Update service.shortlists counter
            cursor.execute(
                "UPDATE service SET shortlists = MAX(0, shortlists - 1) WHERE id = ?",
                (service_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

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

            cursor.execute("""
                SELECT id FROM shortlist
                WHERE homeowner_id = ? AND service_id = ?
            """, (homeOwnerId, serviceId))
            
            #check if already shortlisted.
            if cursor.fetchone():
                return False  

            cursor.execute("""
                INSERT INTO shortlist (homeowner_id, service_id, shortlist_date)
                VALUES (?, ?, DATE('now'))
            """, (homeOwnerId, serviceId))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"[Shortlist.addShortlist] Error: {e}")
            return False
        
    #currently not in user story.    
    @staticmethod
    def removeShortlist(homeOwnerId, serviceId):
        try:
            conn = getDb()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM shortlist
                WHERE homeowner_id = ? AND service_id = ?
            """, (homeOwnerId, serviceId))

            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()

            return rows_affected > 0
        except Exception as e:
            print(f"[Shortlist Entity] Error removing shortlist: {e}")
            return False