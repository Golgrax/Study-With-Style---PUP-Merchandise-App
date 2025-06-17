import sqlite3
import os

def create_profiles_table():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_profiles_table.sql')

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(sql_path, 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)
        
        conn.commit()
        print("Database tables created successfully from SQL file.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Error: Could not find the SQL file at {sql_path}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_profiles_table()