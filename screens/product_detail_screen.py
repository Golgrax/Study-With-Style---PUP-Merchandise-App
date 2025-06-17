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

    def __init__(self, **kwargs):
        super(ProductDetailScreen, self).__init__(**kwargs)
        self.project_root = os.getcwd()
        self.default_img = os.path.join(self.project_root, 'assets', 'question_mark.png')

    def get_image_source(self, db_path):
        """A centralized function to get a valid, absolute image source."""
        if db_path:
            abs_path = os.path.join(self.project_root, db_path)
            if os.path.exists(abs_path):
                return abs_path
        return self.default_img

    def on_pre_enter(self, *args):
        product = self.db_manager.fetch_product_by_id(self.product_id)
        if product:
            self.ids.detail_name.text = product.get('name', 'N/A')
            self.ids.detail_description.text = product.get('description', 'No description available.')
            self.ids.detail_image.source = self.get_image_source(product.get('image_path'))
            self.ids.detail_price.text = f"P{product.get('price', 0):.2f}"
            self.product_id = product.get('id')

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