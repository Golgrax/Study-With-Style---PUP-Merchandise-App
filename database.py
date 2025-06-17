import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database.db')

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def fetch_user(self, username):
        conn = self.get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    def user_exists(self, username, email):
        conn = self.get_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        conn.close()
        return existing_user is not None

    def insert_user(self, name, email, username, password_hash):
        conn = self.get_connection()
        try:
            conn.execute(
                "INSERT INTO users (name, email, username, password_hash) VALUES (?, ?, ?, ?)",
                (name, email, username, password_hash)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return False
        conn.close()
        return True

    def fetch_best_seller(self):
        conn = self.get_connection()
        best_seller = conn.execute('SELECT * FROM products ORDER BY stock_quantity DESC LIMIT 1').fetchone()
        conn.close()
        return best_seller

    def fetch_other_products(self, exclude_id, limit=5):
        conn = self.get_connection()
        other_products = conn.execute('SELECT * FROM products WHERE id != ? LIMIT ?', (exclude_id, limit)).fetchall()
        conn.close()
        return other_products

    def fetch_product_by_id(self, product_id):
        conn = self.get_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        conn.close()
        return product

    def fetch_profile(self, username):
        conn = self.get_connection()
        profile = conn.execute('SELECT name, address1, contact1, address2, contact2 FROM profiles WHERE username = ?', (username,)).fetchone()
        conn.close()
        return profile

    def update_profile(self, username, name, address1, contact1, address2, contact2):
        conn = self.get_connection()
        try:
            conn.execute('''
                INSERT INTO profiles (username, name, address1, contact1, address2, contact2)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(username) DO UPDATE SET
                    name=excluded.name,
                    address1=excluded.address1,
                    contact1=excluded.contact1,
                    address2=excluded.address2,
                    contact2=excluded.contact2
            ''', (username, name, address1, contact1, address2, contact2))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            conn.close()
            return False
        conn.close()
        return True
