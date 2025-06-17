import os
from auth_utils import generate_password_hash
from database import DatabaseManager

def create_admin_user():
    db_manager = DatabaseManager()
    name = "Administrator"
    email = "admin@app.com"
    username = "admin"
    password = "admin"
    password_hash = generate_password_hash(password)
    if not db_manager.user_exists(username, email):
        success = db_manager.insert_user(name, email, username, password_hash, is_admin=1)
        if success:
            print(f"Admin user '{username}' created successfully.")
        else:
            print(f"Failed to create admin user '{username}'.")
    else:
        print(f"Admin user '{username}' already exists.")

if __name__ == '__main__':
    from create_profiles_table import create_profiles_table
    create_profiles_table()
    create_admin_user()
