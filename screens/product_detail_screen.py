from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from database import DatabaseManager
import os

class ProductDetailScreen(Screen):
    product_id = NumericProperty()
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        product = self.db_manager.fetch_product_by_id(self.product_id)
        if product:
            default_img = os.path.join(os.path.dirname(__file__), '..', '..', 'pup_study_style', 'static', 'assets', 'question_mark.png')
            
            self.ids.detail_name.text = product['name']
            self.ids.detail_description.text = product['description'] if 'description' in product.keys() else 'No description available.'
            
            img_path = product['image_path'] if 'image_path' in product.keys() else None
            self.ids.detail_image.source = img_path if img_path and os.path.exists(img_path.replace('../', '')) else default_img
            
            self.ids.detail_price.text = f"P{product['price']:.2f}"
            self.product_id = product['id']

    def add_to_cart(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        Popup(title="Added to Cart",
              content=Label(text="Product added to cart."),
              size_hint=(0.6, 0.2)).open()
              
    def buy_now(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        self.manager.current = 'checkout'