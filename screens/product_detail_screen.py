from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from database import DatabaseManager
import os

class ProductDetailScreen(Screen):
    product_id = NumericProperty(0)
    db_manager = DatabaseManager()

    def __init__(self, **kwargs):
        super(ProductDetailScreen, self).__init__(**kwargs)
        self.project_root = os.getcwd()
        self.default_img = os.path.join(self.project_root, 'assets', 'question_mark.png')

    def get_image_source(self, db_path):
        if db_path and os.path.exists(os.path.join(self.project_root, db_path)):
            return os.path.join(self.project_root, db_path)
        return self.default_img

    def on_pre_enter(self, *args):
        if self.product_id == 0:
            return

        product = self.db_manager.fetch_product_by_id(self.product_id)
        if product:
            self.ids.detail_name.text = product['name']
            self.ids.detail_description.text = product['description'] or 'No description available.'
            image_path = product['image_path'] if 'image_path' in product.keys() else None
            self.ids.detail_image.source = self.get_image_source(image_path)
            self.ids.detail_price.text = f"P{product['price']:.2f}"

    def add_to_cart(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        Popup(title="Added to Cart",
              content=Label(text="Product added to your cart."),
              size_hint=(0.6, 0.2)).open()
              
    def buy_now(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        self.manager.current = 'checkout'
