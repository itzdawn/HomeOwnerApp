"""
Database Initialization Script
This script runs all database creation and population scripts in the correct order.
"""

import os
import sys
import time

# Make sure the current directory is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import the individual scripts
from CreateUsers import dropUserTable, generateAndInsert, viewTable as viewUsers
from CreateUserProfile import create_user_profile_table
from CreateCategory import dropTable as dropCategoryTable, createCategoryTable, createCategories, viewTable as viewCategories
from CreateServices import dropServiceTable, createServiceTables, createFakeServices, viewTable as viewServices
from CreateShortlists import dropTable as dropShortlistTable, createShortlistTables, createFakeShortlists, viewTable as viewShortlists
from CreateCompletedServices import dropTable as dropCompletedServicesTable, createCompletedServiceTable, createFakeCompletedServices, viewTable as viewCompletedServices

# Configure the number of entries to generate
# Ensure we have more users than needed for services, shortlists, etc.
NUM_USERS = 150
NUM_SERVICES = 100
NUM_SHORTLISTS = 70
NUM_COMPLETED_SERVICES = 80

def ensure_db_directory_exists():
    """Ensure the database directory exists"""
    db_dir = os.path.join(script_dir)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, 'app.db')

def initialize_database():
    """Run all database initialization steps in the correct order"""
    print("\n" + "="*80)
    print("INITIALIZING DATABASE")
    print("="*80 + "\n")
    
    db_path = ensure_db_directory_exists()
    print(f"Database will be created at: {db_path}\n")
    
    print("\n" + "="*30 + " STEP 1: Creating Users " + "="*30)
    # Drop and recreate user table
    dropUserTable()
    generateAndInsert(NUM_USERS)
    print("\nCreated users:")
    viewUsers()
    
    print("\n" + "="*30 + " STEP 2: Creating User Profiles " + "="*30)
    # Create user profiles
    create_user_profile_table()
    
    print("\n" + "="*30 + " STEP 3: Creating Service Categories " + "="*30)
    # Drop and recreate service categories
    dropCategoryTable()
    createCategoryTable()
    createCategories()
    print("\nCreated categories:")
    viewCategories()
    
    # Ensure we have the necessary roles before proceeding
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check if we have HomeOwner and Cleaner users
    cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'HomeOwner'")
    home_owner_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'Cleaner'")
    cleaner_count = cursor.fetchone()[0]
    conn.close()
    
    if home_owner_count == 0 or cleaner_count == 0:
        print("\n" + "!"*80)
        print(f"WARNING: Not enough users with required roles. HomeOwners: {home_owner_count}, Cleaners: {cleaner_count}")
        print("Adding more users with these roles...")
        print("!"*80 + "\n")
        
        # Add some users with specific roles
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Add HomeOwners if needed
        if home_owner_count < 10:
            print("Adding HomeOwner users...")
            for i in range(1, 11):
                username = f"homeowner_{i}"
                if not is_username_used(cursor, username):
                    cursor.execute("INSERT INTO user (username, password, role, status) VALUES (?, ?, ?, ?)", 
                               (username, f"password_{i}", "HomeOwner", 1))
        
        # Add Cleaners if needed
        if cleaner_count < 10:
            print("Adding Cleaner users...")
            for i in range(1, 11):
                username = f"cleaner_{i}"
                if not is_username_used(cursor, username):
                    cursor.execute("INSERT INTO user (username, password, role, status) VALUES (?, ?, ?, ?)", 
                               (username, f"password_{i}", "Cleaner", 1))
        
        conn.commit()
        conn.close()
        
        # Update user profiles for the new users
        print("Updating user profiles for new users...")
        create_user_profile_table()
    
    print("\n" + "="*30 + " STEP 4: Creating Services " + "="*30)
    # Drop and recreate services
    dropServiceTable()
    createServiceTables()
    createFakeServices(NUM_SERVICES)
    print("\nCreated services:")
    viewServices()
    
    print("\n" + "="*30 + " STEP 5: Creating Shortlists " + "="*30)
    # Drop and recreate shortlists
    dropShortlistTable()
    createShortlistTables()
    createFakeShortlists(NUM_SHORTLISTS)
    print("\nCreated shortlists:")
    viewShortlists()
    
    print("\n" + "="*30 + " STEP 6: Creating Completed Services " + "="*30)
    # Drop and recreate completed services
    dropCompletedServicesTable()
    createCompletedServiceTable()
    createFakeCompletedServices(NUM_COMPLETED_SERVICES)
    print("\nCreated completed services:")
    viewCompletedServices()
    
    print("\n" + "="*80)
    print("DATABASE INITIALIZATION COMPLETE")
    print("="*80 + "\n")

def is_username_used(cursor, username):
    """Check if a username already exists in the database"""
    cursor.execute("SELECT COUNT(*) FROM user WHERE username = ?", (username,))
    return cursor.fetchone()[0] > 0

if __name__ == "__main__":
    start_time = time.time()
    initialize_database()
    end_time = time.time()
    print(f"Total initialization time: {end_time - start_time:.2f} seconds") 