from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
import os

class CartScreen(Screen):
    def __init__(self, **kwargs):
        super(CartScreen, self).__init__(**kwargs)
        # Get the directory where main.py is running from (our project root)
        self.project_root = os.getcwd() 
        # Build the correct absolute path to the assets folder
        self.assets_path = os.path.join(self.project_root, 'assets')
        self.default_img = os.path.join(self.assets_path, 'question_mark.png')

    def get_image_source(self, db_path):
        """A centralized function to get a valid, absolute image source."""
        if db_path:
            full_path_to_check = os.path.join(self.project_root, db_path)
            if os.path.exists(full_path_to_check):
                return full_path_to_check
        return self.default_img

    def on_pre_enter(self, *args):
        self.populate_cart()

    def populate_cart(self):
        cart_list = self.ids.cart_list
        cart_list.clear_widgets()
        app = App.get_running_app()
        total_price = 0

        if not app.cart:
            cart_list.add_widget(Label(text="Your cart is empty.", font_size='18sp', color=(0.2, 0.2, 0.2, 1)))
            self.ids.total_label.text = "Total: P0.00"
            return

        for item in app.cart:
            product = app.get_product_by_id(item['product_id'])
            if product:
                item_layout = self.create_cart_item_widget(item, product)
                cart_list.add_widget(item_layout)
                total_price += product['price'] * item['quantity']
        
        self.ids.total_label.text = f"Total: P{total_price:.2f}"

    def create_cart_item_widget(self, item, product):
        item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=10, spacing=10)
        
        image_path = product['image_path'] if 'image_path' in product.keys() else None
        product_image = Image(source=self.get_image_source(image_path), size_hint_x=None, width='80dp')
        
        details_layout = BoxLayout(orientation='vertical')
        product_label = Label(text=f"{product['name']}", font_size='16sp', halign='left', valign='top', color=(0.1, 0.1, 0.1, 1))
        product_label.bind(size=product_label.setter('text_size'))
        price_label = Label(text=f"P{product['price']:.2f}", font_size='14sp', halign='left', valign='top', color=(0.1, 0.1, 0.1, 1))
        details_layout.add_widget(product_label)
        details_layout.add_widget(price_label)

        quantity_controls = BoxLayout(orientation='horizontal', size_hint_x=None, width='120dp')
        btn_decrease = Button(text='-', size_hint_x=None, width='40dp', on_release=lambda x, i=item: self.decrease_quantity(i))
        quantity_label = Label(text=str(item['quantity']), size_hint_x=None, width='40dp', color=(0.1, 0.1, 0.1, 1))
        btn_increase = Button(text='+', size_hint_x=None, width='40dp', on_release=lambda x, i=item: self.increase_quantity(i))
        quantity_controls.add_widget(btn_decrease)
        quantity_controls.add_widget(quantity_label)
        quantity_controls.add_widget(btn_increase)

        item_layout.add_widget(product_image)
        item_layout.add_widget(details_layout)
        item_layout.add_widget(quantity_controls)
        return item_layout

    def decrease_quantity(self, item):
        app = App.get_running_app()
        if item['quantity'] > 1:
            item['quantity'] -= 1
        else:
            app.cart.remove(item)
        self.populate_cart()

    def increase_quantity(self, item):
        item['quantity'] += 1
        self.populate_cart()