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
        
        total_price = 0
        total_quantity = 0
        for item in cart:
            product = app.get_product_by_id(item['product_id'])
            if product:
                total_price += product['price'] * item['quantity']
                total_quantity += item['quantity']
        
        ref_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        db_manager = DatabaseManager()
        conn = db_manager.get_connection()
        try:
            conn.execute(
                "INSERT INTO orders (ref_no, username, total_price, quantity, payment, status) VALUES (?, ?, ?, ?, ?, ?)",
                (ref_no, app.current_user, total_price, total_quantity, "Cash on Delivery", "Pending")
            )
            conn.commit()
            
            app.cart.clear()
            
            success_popup = Popup(title="Order Placed",
                                  content=Label(text=f"Your order has been placed!\nReference No: {ref_no}"),
                                  size_hint=(0.8, 0.4))
            success_popup.open()
            
            self.manager.current = 'home'
            
        except Exception as e:
            print(f"Error placing order: {e}")
            Popup(title="Error",
                  content=Label(text="Could not place your order. Please try again."),
                  size_hint=(0.8, 0.3)).open()
        finally:
            if conn:
                conn.close()
