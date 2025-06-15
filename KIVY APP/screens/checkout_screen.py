from kivy.app import App
from kivy.uix.screenmanager import Screen

class CheckoutScreen(Screen):
    def on_pre_enter(self, *args):
        self.update_order_summary()

    def update_order_summary(self):
        app = App.get_running_app()
        cart = app.cart
        if not cart:
            self.ids.order_summary.text = "Your cart is empty."
            return

        total_price = 0
        summary_lines = []
        for item in cart:
            product = app.get_product_by_id(item['product_id'])
            if product:
                # ** THE FIX IS HERE **
                line_price = product['price'] * item['quantity']
                line = f"{product['name']} x {item['quantity']} = P{line_price:.2f}"
                summary_lines.append(line)
                total_price += line_price

        summary_text = "\n".join(summary_lines)
        summary_text += f"\n\nTotal: P{total_price:.2f}"
        self.ids.order_summary.text = summary_text

    def place_order(self):
        app = App.get_running_app()
        print("Placing order for:", app.cart)
        app.cart = [] # Clear the cart
        app.root.current = 'home'