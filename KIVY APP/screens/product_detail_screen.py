from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from database import DatabaseManager

class ProductDetailScreen(Screen):
    product_id = NumericProperty()
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        product = self.db_manager.fetch_product_by_id(self.product_id)
        if product:
            self.ids.detail_name.text = product['name']
            self.ids.detail_description.text = product.get('description', 'No description available.')
            self.ids.detail_image.source = product.get('image_path', 'path/to/default.png')
            self.ids.detail_price.text = f"₱{product.get('price', 0):.2f}"
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