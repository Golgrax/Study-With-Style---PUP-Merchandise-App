import sqlite3
import os
from auth_utils import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def create_admin_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    name = "Administrator"
    email = "admin@app.com"
    username = "admin"
    password = "admin"
    password_hash = generate_password_hash(password)
    is_admin = 1
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        try:
            cursor.execute(
                "INSERT INTO users (name, email, username, password_hash, is_admin) VALUES (?, ?, ?, ?, ?)",
                (name, email, username, password_hash, is_admin)
            )
            conn.commit()
            print(f"Admin user '{username}' created successfully.")
        except sqlite3.IntegrityError:
            print(f"Admin user '{username}' or email '{email}' already exists.")
    else:
        print(f"Admin user '{username}' already exists.")
    conn.close()

if __name__ == '__main__':
    from create_profiles_table import create_profiles_table
    create_profiles_table()
    create_admin_user()