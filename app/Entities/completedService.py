import sqlite3
from datetime import datetime
from flask import current_app


def getDb():
    db = current_app.config['DATABASE']
    conn = sqlite3.connect(db)
    return conn

class CompletedService:
    def __init__(self, id=None, cleanerId=None, homeOwnerId=None, serviceId=None, serviceDate=None):
        self.__id = id
        self.__cleanerId = cleanerId
        self.__homeOwnerId = homeOwnerId
        self.__serviceId = serviceId
        self.serviceDate = serviceDate if serviceDate else datetime.now().strftime("%d-%m-%Y")
    
    def getId(self):
        return self.__id
    def getHomeOwnerId(self):
        return self.__homeOwnerId
    def getCleanerId(self):
        return self.__cleanerId
    def getServiceId(self):
        return self.__serviceId
    
    # def completeService(self):
    #     conn = getDb()
    #     cursor = conn.cursor()
    #     cursor.execute("INSERT INTO completed_service (cleaner_id, homeowner_id, service_id, service_date) VALUES (?,?,?,?)", 
    #                    (self.getCleanerId, self.getHomeOwnerId, self.getServiceId, self.serviceDate))
    #     conn.commit()
    #     conn.close()
    
    
    @staticmethod
    def getAllPastServices(cleanerId):
        """
        Return a list of dict
        """
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT 
                    cs.id AS CompletedServiceId,
                    cs.cleaner_id,
                    cs.homeowner_id,
                    cs.service_id,
                    cs.service_date,
                    s.name,
                    s.description,
                    s.price,
                    s.category_id,
                    sc.name AS category_name,
                    u.username AS homeowner_name,
                    s.creation_date
                FROM completed_service cs
                JOIN service s ON cs.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                LEFT JOIN user u ON cs.homeowner_id = u.id
                WHERE cs.cleaner_id = ?
                ORDER BY cs.service_date DESC
            """

            cursor.execute(query, (cleanerId,))
            results = cursor.fetchall()
            conn.close()

            return [dict(result) for result in results]
        except Exception as e:
            print(f"[getAllPastServices] Error: {str(e)}")
            return []
        
    @staticmethod
    def searchPastServices(cleanerId, startDate=None, endDate=None, category_id=None, name=None):
        conn = getDb()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        query = """ 
            SELECT 
                cs.id AS CompletedServiceId, 
                cs.cleaner_id, 
                cs.homeowner_id, 
                cs.service_id, 
                cs.service_date,
                s.name, 
                s.description, 
                s.price, 
                s.category_id,
                sc.name as category_name,
                u.username as homeowner_name,
                s.creation_date
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            LEFT JOIN service_category sc ON s.category_id = sc.id
            LEFT JOIN user u ON cs.homeowner_id = u.id
            WHERE cs.cleaner_id = ?
        """

        params = [cleanerId]
        if startDate:
            query += " AND cs.service_date >= ?"
            params.append(startDate)
        if endDate:
            query += " AND cs.service_date <= ?"
            params.append(endDate)
        if category_id:
            query += " AND s.category_id = ?"
            params.append(category_id)
        if name:
            query += " AND LOWER(s.name) LIKE ?"
            params.append(f"%{name.lower()}%")

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        conn.close()

        return [dict(result) for result in results]

    @staticmethod
    def getPastServiceById(serviceId):
        conn = None
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT 
                    cs.id AS CompletedServiceId,
                    cs.cleaner_id,
                    cs.homeowner_id,
                    cs.service_id,
                    cs.service_date,
                    s.name,
                    s.description,
                    s.price,
                    s.category_id,
                    sc.name AS category_name,
                    u.username AS homeowner_name,
                    s.creation_date
                FROM completed_service cs
                JOIN service s ON cs.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                LEFT JOIN user u ON cs.homeowner_id = u.id
                WHERE cs.id = ?
            """

            cursor.execute(query, (serviceId,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None

        except Exception as e:
            print(f"[CompletedService.getPastServiceById] Error: {e}")
            return None