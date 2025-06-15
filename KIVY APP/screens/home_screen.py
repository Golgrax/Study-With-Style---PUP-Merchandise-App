from kivy.uix.screenmanager import Screen
from database import DatabaseManager
from widgets.product_item import ProductItem

class HomeScreen(Screen):
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        best_seller = self.db_manager.fetch_best_seller()
        if best_seller:
            best_seller_image = self.ids.get('best_seller_image')
            best_seller_label = self.ids.get('best_seller_label')
            if best_seller_image:
                best_seller_image.source = best_seller['image_path'] if 'image_path' in best_seller.keys() else 'path/to/default.png'
            if best_seller_label:
                best_seller_label.text = best_seller['name']
        self.populate_other_products(best_seller['id'] if best_seller else -1)

    def populate_other_products(self, exclude_id):
        product_list = self.ids.get('product_list')
        if not product_list:
            return
        product_list.clear_widgets()
        other_products = self.db_manager.fetch_other_products(exclude_id)
        for product in other_products:
            item = ProductItem(
                product_id=product['id'],
                product_name=product['name'],
                product_price=f"Price: ₱{product['price']:.2f}",
                image_source=product['image_path'] if 'image_path' in product.keys() else 'path/to/default.png'
            )
            product_list.add_widget(item)
