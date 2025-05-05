import sqlite3
import os
import random
from datetime import datetime

def create_user_profile_table():
    try:
        # Get the database path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'app.db')
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create user_profile table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
        ''')
        
        conn.commit()
        print("User profile table created successfully")
        
        # Get existing user profiles
        cursor.execute("SELECT * FROM user_profile")
        existing_profiles = cursor.fetchall()
        
        if len(existing_profiles) == 0:
            # Insert sample data if no profiles exist
            insert_sample_profiles(cursor)
            conn.commit()
        
        # Display all user profiles
        display_user_profiles(cursor)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def insert_sample_profiles(cursor):
    # First, get all users from the user table
    cursor.execute("SELECT id, username, role FROM user")
    users = cursor.fetchall()
    
    # Sample data for profiles
    sample_profiles = []
    
    for user in users:
        user_id = user[0]
        username = user[1]
        role = user[2]
        
        # Skip if user already has a profile
        cursor.execute("SELECT id FROM user_profile WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            continue
        
        # Generate sample profile data based on role
        if role == "Admin":
            full_name = f"Admin {username.capitalize()}"
            phone = f"+1 (800) 555-{random.randint(1000, 9999)}"
            address = f"{random.randint(100, 999)} Admin Street, Admin City, AC {random.randint(10000, 99999)}"
        elif role == "Cleaner":
            full_name = f"{username.split('_')[0].capitalize()} {username.split('_')[-1].capitalize() if '_' in username else 'Cleaner'}"
            phone = f"+1 (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
            address = f"{random.randint(100, 999)} Cleaner Ave, Service City, SC {random.randint(10000, 99999)}"
        elif role == "HomeOwner":
            full_name = f"{username.split('_')[0].capitalize()} {username.split('_')[-1].capitalize() if '_' in username else 'Owner'}"
            phone = f"+1 (777) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
            address = f"{random.randint(100, 999)} Home Street, Residence City, RC {random.randint(10000, 99999)}"
        else:
            full_name = f"{username.capitalize()} User"
            phone = f"+1 (444) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
            address = f"{random.randint(100, 999)} Platform Road, System City, PC {random.randint(10000, 99999)}"
        
        sample_profiles.append((user_id, full_name, phone, address))
    
    # Insert the sample profiles
    for profile in sample_profiles:
        cursor.execute('''
        INSERT INTO user_profile (user_id, full_name, phone, address)
        VALUES (?, ?, ?, ?)
        ''', profile)
    
    print(f"Inserted {len(sample_profiles)} sample user profiles")

def display_user_profiles(cursor):
    # Get all profiles with user information
    cursor.execute('''
    SELECT up.id, up.user_id, u.username, u.role, up.full_name, up.phone, up.address
    FROM user_profile up
    JOIN user u ON up.user_id = u.id
    ORDER BY up.id
    ''')
    
    profiles = cursor.fetchall()
    
    print("\n=== USER PROFILES ===")
    print(f"Total profiles: {len(profiles)}")
    print("-" * 100)
    print(f"{'ID':<5} {'USER_ID':<8} {'USERNAME':<15} {'ROLE':<15} {'FULL_NAME':<20} {'PHONE':<15} {'ADDRESS':<30}")
    print("-" * 100)
    
    for profile in profiles:
        profile_id, user_id, username, role, full_name, phone, address = profile
        print(f"{profile_id:<5} {user_id:<8} {username:<15} {role:<15} {full_name:<20} {phone:<15} {address[:30]:<30}")
    
    print("-" * 100)

if __name__ == "__main__":
    create_user_profile_table() 