from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button

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
            self.ids.total_label.text = "Total: ₱0.00"
            return

        for item in app.cart:
            product = app.get_product_by_id(item['product_id'])
            if product:
                item_layout = self.create_cart_item_widget(item, product)
                cart_list.add_widget(item_layout)
                total_price += product['price'] * item['quantity']
        
        self.ids.total_label.text = f"Total: ₱{total_price:.2f}"

    def create_cart_item_widget(self, item, product):
        app = App.get_running_app()
        item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=10, spacing=10)
        
        img_src = product.get('image_path', 'path/to/default.png')
        product_image = Image(source=img_src, size_hint_x=None, width='80dp', allow_stretch=True, keep_ratio=True)

        details_layout = BoxLayout(orientation='vertical')
        product_label = Label(text=f"{product['name']}", font_size='16sp', halign='left', valign='top')
        product_label.bind(size=product_label.setter('text_size'))
        
        price_label = Label(text=f"₱{product['price']:.2f}", font_size='14sp', halign='left', valign='top')
        price_label.bind(size=price_label.setter('text_size'))
        details_layout.add_widget(product_label)
        details_layout.add_widget(price_label)
        quantity_controls = BoxLayout(orientation='horizontal', size_hint_x=None, width='120dp')
        btn_decrease = Button(text='-', size_hint_x=None, width='40dp', on_release=lambda x: self.decrease_quantity(item))
        quantity_label = Label(text=str(item['quantity']), size_hint_x=None, width='40dp')
        btn_increase = Button(text='+', size_hint_x=None, width='40dp', on_release=lambda x: self.increase_quantity(item))
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