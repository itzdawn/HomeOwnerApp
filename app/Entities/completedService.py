import sqlite3
from datetime import datetime, timedelta
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

    @classmethod
    def generateReport(cls, reportType, dateValue, groupBy):
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            baseDate = datetime.strptime(dateValue, "%Y-%m-%d")

            if reportType == 'daily':
                startDate = endDate = baseDate
            elif reportType == 'weekly':
                startDate = baseDate - timedelta(days=baseDate.weekday())
                endDate = startDate + timedelta(days=6)
            elif reportType == 'monthly':
                startDate = baseDate.replace(day=1)
                nextMonth = startDate.replace(day=28) + timedelta(days=4)
                endDate = nextMonth - timedelta(days=nextMonth.day)
            else:
                raise ValueError("Unsupported reportType")

            joins = ""
            groupField = ""

            if groupBy == 'category':
                joins = """
                    JOIN service s ON cs.service_id = s.id
                    JOIN service_category c ON s.category_id = c.id
                """
                groupField = "c.name"
            elif groupBy == 'service':
                joins = "JOIN service s ON cs.service_id = s.id"
                groupField = "s.name"
            elif groupBy == 'cleaner':
                joins = "JOIN user u ON cs.cleaner_id = u.id"
                groupField = "u.username"
            elif groupBy == 'homeowner':
                joins = "JOIN user u ON cs.homeowner_id = u.id"
                groupField = "u.username"
            else:
                raise ValueError("Invalid groupBy parameter")

            query = f"""
                SELECT {groupField} AS groupKey, COUNT(*) AS totalServicesUsed
                FROM completed_service cs
                {joins}
                WHERE DATE(cs.service_date) BETWEEN ? AND ?
                GROUP BY {groupField}
                ORDER BY totalServicesUsed DESC
            """

            params = [startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")]
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                return []

            return [{'groupKey': row['groupKey'], 'totalServicesUsed': row['totalServicesUsed']} for row in rows]

        except Exception as e:
            print("Error in generateReport:", e)
            return None

        
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