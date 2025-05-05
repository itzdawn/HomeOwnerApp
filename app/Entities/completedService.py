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
    
    def completeService(self):
        conn = getDb()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO completed_service (cleaner_id, homeowner_id, service_id, service_date) VALUES (?,?,?,?)", 
                       (self.getCleanerId, self.getHomeOwnerId, self.getServiceId, self.serviceDate))
        conn.commit()
        conn.close()
    
    @staticmethod
    def searchPastServices(cleanerId, startDate=None, endDate=None, category=None):
        conn = getDb()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        query = """ SELECT cs.id AS CompletedServiceId, cs.cleaner_id, cs.homeowner_id, cs.service_id, cs.service_date,
            s.name, s.description, s.price, s.category, s.creation_date
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            WHERE cs.cleaner_id = ?
            """
        params = [cleanerId]
        if startDate:
            query += " AND cs.service_date >= ?"
            params.append(startDate)
        if endDate:
            query += " AND cs.service_date <= ?"
            params.append(endDate)
        if category:
            query += " AND s.category = ?"
            params.append(category)
            
        cursor.execute(query, tuple(params))
        queryResults = cursor.fetchall()
        conn.close()
        return [dict(result) for result in queryResults]

    @staticmethod
    def get_service_report(start_date, end_date, group_by="category"):
        """
        Generate a service usage report between given dates
        
        Args:
            start_date (str): Start date for report period (format: YYYY-MM-DD)
            end_date (str): End date for report period (format: YYYY-MM-DD)
            group_by (str): How to group the data - 'category', 'service', 'cleaner', 'homeowner'
            
        Returns:
            dict: Report data including rows and totals
        """
        conn = getDb()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Base query - will be modified based on group_by
        query = """
            SELECT {select_fields}
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            JOIN user u1 ON cs.cleaner_id = u1.id
            JOIN user u2 ON cs.homeowner_id = u2.id
            WHERE cs.service_date BETWEEN ? AND ?
            GROUP BY {group_by_field}
            ORDER BY {order_by}
        """
        
        # Set query parameters based on group_by
        if group_by == "category":
            select_fields = """
                s.category,
                COUNT(cs.id) AS service_count, 
                SUM(s.price) AS total_revenue
            """
            group_by_field = "s.category"
            order_by = "total_revenue DESC"
        
        elif group_by == "service":
            select_fields = """
                s.name,
                COUNT(cs.id) AS booking_count,
                SUM(s.price) AS total_revenue
            """
            group_by_field = "s.id"
            order_by = "booking_count DESC"
        
        elif group_by == "cleaner":
            select_fields = """
                u1.name as cleaner_name,
                COUNT(cs.id) AS service_count,
                SUM(s.price) AS total_revenue
            """
            group_by_field = "cs.cleaner_id"
            order_by = "service_count DESC"
        
        elif group_by == "homeowner":
            select_fields = """
                u2.name as homeowner_name,
                COUNT(cs.id) AS service_count,
                SUM(s.price) AS total_spent
            """
            group_by_field = "cs.homeowner_id"
            order_by = "service_count DESC"
        
        else:
            # Default to category if invalid group_by
            select_fields = """
                s.category,
                COUNT(cs.id) AS service_count, 
                SUM(s.price) AS total_revenue
            """
            group_by_field = "s.category"
            order_by = "total_revenue DESC"
        
        # Format the query with the fields
        query = query.format(
            select_fields=select_fields,
            group_by_field=group_by_field,
            order_by=order_by
        )
        
        # Execute query
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        
        # Get totals
        totals_query = """
            SELECT 
                COUNT(cs.id) AS total_count,
                SUM(s.price) AS total_revenue
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            WHERE cs.service_date BETWEEN ? AND ?
        """
        cursor.execute(totals_query, (start_date, end_date))
        total_result = cursor.fetchone()
        conn.close()
        
        # Format results for report
        rows = []
        for result in results:
            row = []
            for key in result.keys():
                row.append(result[key])
            rows.append(row)
        
        # Format totals
        if group_by == "category" or group_by == "service" or group_by == "cleaner":
            totals = ["Total", total_result['total_count'], total_result['total_revenue']]
        else:  # homeowner
            totals = ["Total", total_result['total_count'], total_result['total_revenue']]
        
        return {
            "rows": rows,
            "totals": totals
        }

    @staticmethod
    def getPastServiceById(serviceId, cleanerId):
        """
        Get a single completed service by ID with detailed information
        
        Args:
            serviceId (int): ID of the completed service
            cleanerId (int): ID of the cleaner (for authorization)
            
        Returns:
            dict: Dictionary containing service details or None if not found
        """
        conn = getDb()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # Comprehensive query to get all needed information including homeowner details and ratings
        query = """
            SELECT 
                cs.id, 
                cs.cleaner_id, 
                cs.homeowner_id, 
                cs.service_id, 
                cs.service_date,
                s.name, 
                s.description, 
                s.price, 
                s.category as category_id,
                cat.name as category_name,
                s.duration,
                u.name as homeowner_name,
                a.street || ', ' || a.city || ', ' || a.state || ' ' || a.zip as address,
                COALESCE(AVG(r.rating), 0) as rating,
                r.feedback
            FROM completed_service cs
            JOIN service s ON cs.service_id = s.id
            LEFT JOIN category cat ON s.category = cat.id
            JOIN user u ON cs.homeowner_id = u.id
            LEFT JOIN address a ON u.id = a.user_id
            LEFT JOIN rating r ON cs.id = r.completed_service_id
            WHERE cs.id = ? AND cs.cleaner_id = ?
            GROUP BY cs.id
        """
        
        cursor.execute(query, (serviceId, cleanerId))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return dict(result)
        return None

    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # cleaner_id INTEGER NOT NULL,
    # homeowner_id INTEGER NOT NULL,
    # service_id INTEGER NOT NULL,
    # service_date TEXT NOT NULL,
    # FOREIGN KEY (cleaner_id) REFERENCES user(id),
    # FOREIGN KEY (homeowner_id) REFERENCES user(id),
    # FOREIGN KEY (service_id) REFERENCES service(id)