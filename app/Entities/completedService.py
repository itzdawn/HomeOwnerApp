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
    def searchPastServices(cleanerId, startDate=None, endDate=None, category_id=None):
        """
        Search for past services completed by a cleaner with optional filters
        
        Args:
            cleanerId (int): ID of the cleaner
            startDate (str, optional): Start date for filtering
            endDate (str, optional): End date for filtering
            category_id (int, optional): Category ID for filtering
            
        Returns:
            list: List of dictionaries representing completed services
        """
        conn = getDb()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # Enhanced query to include homeowner name and category details
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
            
        # Log query for debugging
        print(f"DEBUG - SQL Query: {query}")
        print(f"DEBUG - Query params: {params}")
            
        cursor.execute(query, tuple(params))
        queryResults = cursor.fetchall()
        
        # Debug first result
        if queryResults:
            print(f"DEBUG - First raw database result: {dict(queryResults[0])}")
        
        # Convert results to dictionaries and ensure proper data types
        results = []
        for row in queryResults:
            result_dict = dict(row)
            
            # Ensure proper types for category_id
            if 'category_id' in result_dict and result_dict['category_id'] is not None:
                try:
                    if not isinstance(result_dict['category_id'], int):
                        result_dict['category_id'] = int(result_dict['category_id'])
                except (ValueError, TypeError):
                    # Keep original value if conversion fails
                    pass
            
            results.append(result_dict)
            
        conn.close()
        return results

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
        try:
            conn = getDb()
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            
            # Simplified query to reduce potential for errors
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
                    u.username as homeowner_name
                FROM completed_service cs
                JOIN service s ON cs.service_id = s.id
                LEFT JOIN service_category sc ON s.category_id = sc.id
                LEFT JOIN user u ON cs.homeowner_id = u.id
                WHERE cs.id = ? AND cs.cleaner_id = ?
            """
            
            # Log query for debugging
            print(f"DEBUG - Detail Query for service {serviceId}: {query}")
            print(f"DEBUG - Detail params: {serviceId}, {cleanerId}")
            
            cursor.execute(query, (serviceId, cleanerId))
            result = cursor.fetchone()
            
            # Debug result
            if result:
                result_dict = dict(result)
                print(f"DEBUG - Service detail result: {result_dict}")
                
                # Add additional rating info in a separate query to avoid JOIN issues
                rating_query = """
                    SELECT AVG(rating) as avg_rating, feedback 
                    FROM rating 
                    WHERE completed_service_id = ?
                    GROUP BY completed_service_id
                """
                cursor.execute(rating_query, (serviceId,))
                rating_result = cursor.fetchone()
                
                if rating_result:
                    rating_dict = dict(rating_result)
                    result_dict['rating'] = rating_dict.get('avg_rating', 0)
                    result_dict['feedback'] = rating_dict.get('feedback', '')
                else:
                    result_dict['rating'] = 0
                    result_dict['feedback'] = ''
                
                # Ensure proper types for category_id
                if 'category_id' in result_dict and result_dict['category_id'] is not None:
                    try:
                        if not isinstance(result_dict['category_id'], int):
                            result_dict['category_id'] = int(result_dict['category_id'])
                    except (ValueError, TypeError):
                        # Keep original value if conversion fails
                        pass
                        
                conn.close()
                return result_dict
                
            print(f"DEBUG - No service found with ID {serviceId} for cleaner {cleanerId}")
            conn.close()
            return None
            
        except Exception as e:
            print(f"ERROR in getPastServiceById: {str(e)}")
            import traceback
            print(traceback.format_exc())
            if conn:
                conn.close()
            return None

    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # cleaner_id INTEGER NOT NULL,
    # homeowner_id INTEGER NOT NULL,
    # service_id INTEGER NOT NULL,
    # service_date TEXT NOT NULL,
    # FOREIGN KEY (cleaner_id) REFERENCES user(id),
    # FOREIGN KEY (homeowner_id) REFERENCES user(id),
    # FOREIGN KEY (service_id) REFERENCES service(id)