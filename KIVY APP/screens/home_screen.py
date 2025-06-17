from kivy.app import App
from kivy.uix.screenmanager import Screen
from database import DatabaseManager
from widgets.product_item import ProductItem
import os

class HomeScreen(Screen):
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        user_nav = self.ids.get('user_nav')
        admin_nav = self.ids.get('admin_nav')

        if app.is_admin:
            if user_nav:
                user_nav.height = 0
                user_nav.opacity = 0
                user_nav.disabled = True
            if admin_nav:
                admin_nav.height = '50dp'
                admin_nav.opacity = 1
                admin_nav.disabled = False
        else:
            if user_nav:
                user_nav.height = '50dp'
                user_nav.opacity = 1
                user_nav.disabled = False
            if admin_nav:
                admin_nav.height = 0
                admin_nav.opacity = 0
                admin_nav.disabled = True
        
        best_seller = self.db_manager.fetch_best_seller()
        default_img = os.path.join(os.path.dirname(__file__), '..', '..', 'pup_study_style', 'static', 'assets', 'question_mark.png')
        
        if best_seller:
            best_seller_image = self.ids.get('best_seller_image')
            best_seller_label = self.ids.get('best_seller_label')
            if best_seller_image:
                img_path = best_seller['image_path'] if 'image_path' in best_seller.keys() else None
                if img_path and os.path.exists(str(img_path).replace('../', '')):
                    best_seller_image.source = img_path
                else:
                    best_seller_image.source = default_img
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
            if img_path and os.path.exists(str(img_path).replace('../', '')):
                source = img_path
            else:
                source = default_img
            item = ProductItem(
                product_id=product['id'],
                product_name=product['name'],
                product_price=f"Price: P{product['price']:.2f}",
                image_source=source
            )
            product_list.add_widget(item)
