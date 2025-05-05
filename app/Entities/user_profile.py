import sqlite3
import os
from datetime import datetime

class UserProfile:
    def __init__(self, user_id, full_name, phone, address=None, id=None):
        self.id = id
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        self.address = address
    
    @staticmethod
    def get_db_connection():
        """Get database connection"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_dir, 'app', 'data', 'app.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return None
    
    def to_dict(self):
        """Convert object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address
        }
    
    def save(self):
        """Save profile to database (create or update)"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if self.id:  # Update existing profile
                cursor.execute('''
                UPDATE user_profile 
                SET full_name = ?, phone = ?, address = ?
                WHERE id = ?
                ''', (self.full_name, self.phone, self.address, self.id))
            else:  # Create new profile
                cursor.execute('''
                INSERT INTO user_profile (user_id, full_name, phone, address)
                VALUES (?, ?, ?, ?)
                ''', (self.user_id, self.full_name, self.phone, self.address))
                self.id = cursor.lastrowid
                
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving profile: {str(e)}")
            return False
    
    def delete(self):
        """Delete profile from database"""
        try:
            if not self.id:
                return False
                
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM user_profile WHERE id = ?', (self.id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting profile: {str(e)}")
            return False
    
    @classmethod
    def getUserProfileById(cls, profile_id):
        """Get profile by ID"""
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM user_profile WHERE id = ?', (profile_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return cls(
                    id=row['id'],
                    user_id=row['user_id'],
                    full_name=row['full_name'],
                    phone=row['phone'],
                    address=row['address']
                )
            return None
        except Exception as e:
            print(f"Error getting profile by ID: {str(e)}")
            return None
    
    @classmethod
    def getUserProfileByUserId(cls, user_id):
        """Get profile by user ID"""
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM user_profile WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return cls(
                    id=row['id'],
                    user_id=row['user_id'],
                    full_name=row['full_name'],
                    phone=row['phone'],
                    address=row['address']
                )
            return None
        except Exception as e:
            print(f"Error getting profile by user ID: {str(e)}")
            return None
    
    @classmethod
    def filterProfiles(cls, user_id=None, full_name=None, phone=None):
        """Filter profiles by criteria"""
        try:
            conn = cls.get_db_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM user_profile WHERE 1=1'
            params = []
            
            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)
                
            if full_name:
                query += ' AND full_name LIKE ?'
                params.append(f'%{full_name}%')
                
            if phone:
                query += ' AND phone LIKE ?'
                params.append(f'%{phone}%')
                
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            conn.close()
            
            profiles = []
            for row in rows:
                profile = cls(
                    id=row['id'],
                    user_id=row['user_id'],
                    full_name=row['full_name'],
                    phone=row['phone'],
                    address=row['address']
                )
                profiles.append(profile)
                
            return profiles
        except Exception as e:
            print(f"Error filtering profiles: {str(e)}")
            return [] 