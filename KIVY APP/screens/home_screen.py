from kivy.app import App
from kivy.uix.screenmanager import Screen
from database import DatabaseManager
from widgets.product_item import ProductItem
import os

class HomeScreen(Screen):
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        order_history_btn = self.ids.get('order_history_button')
        contact_us_btn = self.ids.get('contact_us_button')
        back_to_inventory_btn = self.ids.get('back_to_inventory_button')

        if app.is_admin:
            order_history_btn.opacity = 0
            order_history_btn.size_hint_x = 0
            order_history_btn.disabled = True
            
            contact_us_btn.opacity = 0
            contact_us_btn.size_hint_x = 0
            contact_us_btn.disabled = True
            
            back_to_inventory_btn.opacity = 1
            back_to_inventory_btn.size_hint_x = 1
            back_to_inventory_btn.disabled = False
        else:
            order_history_btn.opacity = 1
            order_history_btn.size_hint_x = 1
            order_history_btn.disabled = False
            
            contact_us_btn.opacity = 1
            contact_us_btn.size_hint_x = 1
            contact_us_btn.disabled = False
            
            back_to_inventory_btn.opacity = 0
            back_to_inventory_btn.size_hint_x = 0
            back_to_inventory_btn.disabled = True
             
        best_seller = self.db_manager.fetch_best_seller()
        default_img = os.path.join(os.path.dirname(__file__), '..', '..', 'pup_study_style', 'static', 'assets', 'question_mark.png')
        
        if best_seller:
            best_seller_image = self.ids.get('best_seller_image')
            best_seller_label = self.ids.get('best_seller_label')
            if best_seller_image:
                img_path = best_seller['image_path'] if 'image_path' in best_seller.keys() else None
                best_seller_image.source = img_path if img_path and os.path.exists(img_path.replace('../', '')) else default_img
            if best_seller_label:
                best_seller_label.text = best_seller['name']
        
        self.populate_other_products(best_seller['id'] if best_seller else -1)

    def populate_other_products(self, exclude_id):
        product_list = self.ids.get('product_list')
        if not product_list:
            return
            
        product_list.clear_widgets()
        other_products = self.db_manager.fetch_other_products(exclude_id)
        default_img = os.path.join(os.path.dirname(__file__), '..', '..', 'pup_study_style', 'static', 'assets', 'question_mark.png')
        
        for product in other_products:
            img_path = product['image_path'] if 'image_path' in product.keys() else None
            item = ProductItem(
                product_id=product['id'],
                product_name=product['name'],
                product_price=f"Price: P{product['price']:.2f}",
                image_source=img_path if img_path and os.path.exists(img_path.replace('../', '')) else default_img
            )
            product_list.add_widget(item)