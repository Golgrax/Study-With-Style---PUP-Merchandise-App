from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.lang import Builder
import os

from database import DatabaseManager
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.product_detail_screen import ProductDetailScreen
from screens.cart_screen import CartScreen
from screens.checkout_screen import CheckoutScreen
from screens.profile_screen import ProfileScreen
from screens.edit_profile_screen import EditProfileScreen
from screens.order_history_screen import OrderHistoryScreen
from screens.contact_us_screen import ContactUsScreen
from screens.inventory_management_screen import InventoryManagementScreen

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from create_profiles_table import create_profiles_table

Window.size = (360, 640)
Window.clearcolor = (0.973, 0.957, 0.957, 1)  # Di ko sure kung sakto yung color sa hex na #f8f4f4 but yeah ayan lumabas nung nag covert ako
create_profiles_table()

class StudyWithStyleApp(App):
    current_user = None
    cart = []

    def build(self):
        kv_dir = os.path.join(os.path.dirname(__file__), 'kv')
        for filename in os.listdir(kv_dir):
            if filename.endswith(".kv"):
                Builder.load_file(os.path.join(kv_dir, filename))

        sm = ScreenManager(transition=SlideTransition(direction='left')) # pangit fade mo mico wahaha imma change into this
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProductDetailScreen(name="product_detail"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(CheckoutScreen(name="checkout"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(EditProfileScreen(name="edit_profile"))
        sm.add_widget(OrderHistoryScreen(name="order_history"))
        sm.add_widget(ContactUsScreen(name="contact_us"))
        sm.add_widget(InventoryManagementScreen(name="inventory_management"))
        return sm

    def show_product_detail(self, product_id):
        product_detail_screen = self.root.get_screen('product_detail')
        product_detail_screen.product_id = product_id
        self.root.current = 'product_detail'

    def add_to_cart(self, product_id):
        for item in self.cart:
            if item['product_id'] == product_id:
                item['quantity'] += 1
                break
        else:
            self.cart.append({'product_id': product_id, 'quantity': 1})

    def get_product_by_id(self, product_id):
        db_manager = DatabaseManager()
        return db_manager.fetch_product_by_id(product_id)

    def on_start(self):
        self.cart = []
        self.root.current = 'login'

    def on_profile_button(self):
        if self.current_user:
            self.root.current = 'profile'
        else:
            self.root.current = 'login'

if __name__ == "__main__":
    StudyWithStyleApp().run()
