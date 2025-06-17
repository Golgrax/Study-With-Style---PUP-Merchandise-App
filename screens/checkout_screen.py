from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DatabaseManager
import random
import string

class CheckoutScreen(Screen):
    def on_pre_enter(self, *args):
        self.update_order_summary()

    def update_order_summary(self):
        app = App.get_running_app()
        cart = app.cart
        if not cart:
            self.ids.order_summary.text = "Your cart is empty."
            return

        total_price = 0
        summary_lines = []
        for item in cart:
            product = app.get_product_by_id(item['product_id'])
            if product:
                line_price = product['price'] * item['quantity']
                line = f"{product['name']} x {item['quantity']} = P{line_price:.2f}"
                summary_lines.append(line)
                total_price += line_price

        summary_text = "\n".join(summary_lines)
        summary_text += f"\n\nTotal: P{total_price:.2f}"
        self.ids.order_summary.text = summary_text

    def place_order(self):
        app = App.get_running_app()
        cart = app.cart
        
        if not cart:
            Popup(title="Empty Cart",
                  content=Label(text="Your cart is empty. Cannot place order."),
                  size_hint=(0.8, 0.3)).open()
            return
            
        db_manager = DatabaseManager()
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            for item in cart:
                product_id = item['product_id']
                quantity_ordered = item['quantity']
                cursor.execute("SELECT name, stock_quantity FROM products WHERE id = ?", (product_id,))
                product_data = cursor.fetchone()
                if product_data is None:
                    raise Exception(f"Product with ID {product_id} not found.")
                if product_data['stock_quantity'] < quantity_ordered:
                    raise Exception(f"Not enough stock for {product_data['name']}. "
                                    f"Required: {quantity_ordered}, Available: {product_data['stock_quantity']}")
                new_stock = product_data['stock_quantity'] - quantity_ordered
                cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_stock, product_id))

            total_price = 0
            total_quantity = 0
            for item in cart:
                product = db_manager.fetch_product_by_id(item['product_id'])
                if product:
                    total_price += product['price'] * item['quantity']
                    total_quantity += item['quantity']
            
            ref_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            cursor.execute(
                "INSERT INTO orders (ref_no, username, total_price, quantity, payment, status) VALUES (?, ?, ?, ?, ?, ?)",
                (ref_no, app.current_user, total_price, total_quantity, "Cash on Delivery", "Processing")
            )
            
            conn.commit() 
            app.cart.clear() 
            
            Popup(title="Order Placed",
                  content=Label(text=f"Your order has been placed!\nReference No: {ref_no}"),
                  size_hint=(0.8, 0.4)).open()
            
            self.manager.current = 'home'
            
        except Exception as e:
            conn.rollback()
            print(f"Error placing order: {e}")
            Popup(title="Order Error",
                  content=Label(text=str(e)),
                  size_hint=(0.8, 0.4)).open()
        finally:
            if conn:
                conn.close()
