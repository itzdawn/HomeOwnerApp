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
        self.category_name = None
    
    def getId(self):
        return self.__id
    def getUserId(self):
        return self.__userId
    
    # Convert service object to dictionary for JSON serialization
    def to_dict(self):
        """
        Convert Service object to dictionary for JSON serialization
        """
        # Debug output to see what values we're working with
        print(f"DEBUG - Service object values: id={self.__id}, cleaner_id={self.__userId}, name={self.name}, desc={self.description}, category={self.category}, price={self.price}, category_name={getattr(self, 'category_name', None)}")
        
        # Check if category_name was already populated from JOIN query
        category_name = getattr(self, 'category_name', None)
        
        # If category_name is not yet set but we have a category ID, fetch it
        category_id = self.category
        if category_name is None and category_id is not None:
            try:
                conn = getDb()
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM service_category WHERE id = ?", (category_id,))
                result = cursor.fetchone()
                conn.close()
                if result:
                    category_name = result[0]
                    # Store for future use
                    self.category_name = category_name
            except Exception as e:
                print(f"Error getting category name: {e}")
        
        # Fix potential data type issues
        if not isinstance(category_id, int) and category_id is not None:
            try:
                category_id = int(category_id)
            except (ValueError, TypeError):
                # If conversion fails, keep original value
                pass
        
        # Ensure name is a string, not an integer
        name_value = self.name
        if isinstance(name_value, int):
            name_value = str(name_value)  # Convert integer to string for name field
        
        # Create dictionary with all fields
        service_dict = {
            'id': self.__id,
            'cleaner_id': self.__userId,
            'name': name_value,
            'description': self.description,
            'category_id': category_id,
            'category_name': category_name,  # Include category_name
            'price': self.price,
            'shortlists': self.shortlists,
            'views': self.views,
            'creation_date': self.creationDate
        }
        
        # Debug the final output dictionary
        print(f"DEBUG - Final service dict: id={service_dict['id']}, category_id={service_dict['category_id']}, category_name={service_dict['category_name']}")
        
        return service_dict
    
    #insert to database.
    def createService(self):
        conn = getDb()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO service (cleaner_id, category_id, name, description, price, shortlists, views, creation_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.getUserId(), self.category, self.name, self.description, self.price, self.shortlists, self.views, self.creationDate))
            conn.commit()
            print(f"DEBUG - Service created: {self.name}, category={self.category}")
            return True
        except Exception as e:
            print(f"Error creating service: {e}")
            return False
        finally:
            conn.close()
    
    def updateService(self):
        conn = getDb()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE service
                SET category_id = ?, name = ?, description = ?, price = ?
                WHERE id = ? AND cleaner_id = ?
            """, (self.category, self.name, self.description, self.price, self.__id, self.__userId))
            conn.commit()
            print(f"DEBUG - Service updated: id={self.__id}, category={self.category}")
            return True
        except Exception as e:
            print(f"Error updating service: {e}")
            return False
        finally:
            conn.close()
    
    #retrieve service info by cleanerId from db, return type: list of service objects
    @staticmethod
    def getServiceByUserId(userId):
        conn = getDb()
        cursor = conn.cursor()
        try:
            # Use LEFT JOIN to get category name - consistent with column names
            cursor.execute("""
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.cleaner_id = ?
            """, (userId,))
            results = cursor.fetchall() #list of service tuples
            print(f"DEBUG - Found {len(results)} services for user {userId}")
            
            services = []
            for result in results:
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    category=result[2],
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
        finally:
            conn.close()
    
    #retrieve service info by service id from db
    @staticmethod
    def getServiceByServiceId(serviceId):
        conn = getDb()
        cursor = conn.cursor()
        try:
            # Use LEFT JOIN to get category name - consistent with column names  
            cursor.execute("""
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE s.id = ?
            """, (serviceId,))
            result = cursor.fetchone()
            
            if result:
                print(f"DEBUG - Found service {serviceId}")
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    category=result[2],
                    price=result[5],
                    shortlists=result[6],
                    views=result[7],
                    creationDate=result[8]
                )
                # Store category_name if it exists in the result
                if len(result) > 9:
                    service.category_name = result[9]
                    print(f"DEBUG - Service {result[0]} has category_name: {result[9]}")
                return service
            else:
                print(f"DEBUG - Service {serviceId} not found")
                return None
        except Exception as e:
            print(f"Error getting service by ID: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def deleteService(serviceId, userId):
        """
        Delete a service by ID and cleaner ID
        
        Args:
            serviceId (int): ID of the service to delete
            userId (int): ID of the cleaner for authorization
            
        Returns:
            bool: True if service was deleted, False otherwise
        """
        try:
            conn = getDb()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM service WHERE id = ? AND cleaner_id = ?", (serviceId, userId))
            # Check if any rows were affected by the operation
            rowcount = cursor.rowcount
            conn.commit()
            conn.close()
            # Return True if at least one row was deleted
            return rowcount > 0
        except Exception as e:
            print(f"Error in deleteService: {e}")
            return False
    
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
            
            # Build query dynamically based on provided filters with JOIN to get category name
            query = """
                SELECT s.*, sc.name as category_name
                FROM service s
                LEFT JOIN service_category sc ON s.category_id = sc.id
                WHERE 1=1
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
                
            if category:
                query += " AND s.category_id = ?"
                params.append(category)
            
            print(f"DEBUG - Filter query: {query}")
            print(f"DEBUG - Filter params: {params}")
            
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            
            print(f"DEBUG - Filter returned {len(results)} services")
            
            # Convert to Service objects
            services = []
            for result in results:
                service = Service(
                    id=result[0],
                    userId=result[1],
                    name=result[3],
                    description=result[4],
                    category=result[2],
                    price=result[5],
                    shortlists=result[6],
                    views=result[7],
                    creationDate=result[8]
                )
                # Store category_name as an attribute to access in to_dict
                if len(result) > 9:
                    service.category_name = result[9]
                services.append(service)
            return services
            
        except Exception as e:
            print(f"Error filtering services: {e}")
            return []
        finally:
            if conn:
                conn.close()
