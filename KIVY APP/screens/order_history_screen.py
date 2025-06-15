from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import DatabaseManager

class OrderHistoryScreen(Screen):
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        self.load_order_history()

    def load_order_history(self):
        order_list = self.ids.order_history_list
        order_list.clear_widgets()
        
        app = App.get_running_app()
        username = getattr(app, 'current_user', None)
        if not username:
            order_list.add_widget(Label(text="Please log in to see order history."))
            return

        conn = self.db_manager.get_connection()
        try:
            orders = conn.execute('SELECT ref_no, status, quantity, payment FROM orders WHERE username = ?', (username,)).fetchall()
        except Exception as e:
            print(f"Error fetching orders: {e}")
            order_list.add_widget(Label(text="Could not load order history."))
            orders = []
        finally:
            conn.close()

        if not orders:
            order_list.add_widget(Label(text="No orders found."))
            return

        for order in orders:
            order_list.add_widget(Label(text=str(order['ref_no'])))
            order_list.add_widget(Label(text=str(order['status'])))
            order_list.add_widget(Label(text=str(order['quantity'])))
            order_list.add_widget(Label(text=str(order['payment'])))