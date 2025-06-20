from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

class ProductItem(ButtonBehavior, BoxLayout):
    product_id = NumericProperty()
    product_name = StringProperty()
    product_price = StringProperty()
    image_source = StringProperty()

    def view_details(self):
        app = App.get_running_app()
        app.show_product_detail(self.product_id)

    def add_to_cart(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        Popup(title="Added to Cart",
              content=Label(text=f"'{self.product_name}' added to cart."),
              size_hint=(0.7, 0.2)).open()
        app.root.current = 'cart'

    def buy_now(self):
        app = App.get_running_app()
        app.add_to_cart(self.product_id)
        app.root.current = 'checkout'