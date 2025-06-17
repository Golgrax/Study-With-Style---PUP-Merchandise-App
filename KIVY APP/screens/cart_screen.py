from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
import os

class CartScreen(Screen):
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
        app = App.get_running_app()
        item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=10, spacing=10)
        
        default_img = os.path.join(os.path.dirname(__file__), '..', '..', 'pup_study_style', 'static', 'assets', 'question_mark.png')
        img_src = product['image_path'] if 'image_path' in product.keys() and product['image_path'] and os.path.exists(product['image_path'].replace('../', '')) else default_img
        product_image = Image(source=img_src, size_hint_x=None, width='80dp')

        details_layout = BoxLayout(orientation='vertical')
        product_label = Label(text=f"{product['name']}", font_size='16sp', halign='left', valign='top', color=(0.1, 0.1, 0.1, 1))
        product_label.bind(size=product_label.setter('text_size'))
        
        price_label = Label(text=f"P{product['price']:.2f}", font_size='14sp', halign='left', valign='top')
        price_label.bind(size=price_label.setter('text_size'))
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
        if item['quantity'] > 1:
            item['quantity'] -= 1
        else:
            App.get_running_app().cart.remove(item)
        self.populate_cart()

    def increase_quantity(self, item):
        item['quantity'] += 1
        self.populate_cart()