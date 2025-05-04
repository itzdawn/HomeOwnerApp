import sqlite3
from flask import current_app

def get_db():
    return sqlite3.connect(current_app.config['DATABASE'])

class Shortlist:
    @staticmethod
    def add_to_shortlist(homeowner_id, service_id):
        """Add a service to the homeowner's shortlist and update counters."""
        conn = get_db()
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
        conn = get_db()
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
    def search_shortlisted_services(homeowner_id, keyword=None):
        """Search for shortlisted services with details for a homeowner."""
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT s.*, sc.name as category_name 
            FROM shortlist sl
            JOIN service s ON sl.service_id = s.id
            LEFT JOIN service_category sc ON s.category_id = sc.id
            WHERE sl.homeowner_id = ?
        """
        params = [homeowner_id]
        
        if keyword:
            query += " AND (s.name LIKE ? OR s.description LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    @staticmethod
    def view_shortlisted_services(homeowner_id):
        """View all shortlisted services for a homeowner."""
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT s.*, sc.name as category_name 
            FROM shortlist sl
            JOIN service s ON sl.service_id = s.id
            LEFT JOIN service_category sc ON s.category_id = sc.id
            WHERE sl.homeowner_id = ?
        """
        cursor.execute(query, (homeowner_id,))
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]