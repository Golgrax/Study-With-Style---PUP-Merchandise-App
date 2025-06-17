from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DatabaseManager
from widgets.product_item import ProductItem
import os

class HomeScreen(Screen):
    db_manager = DatabaseManager()
    best_seller_id = None

    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    assets_path = os.path.join(project_root, 'pup_study_style', 'static', 'assets')
    default_img = os.path.join(assets_path, 'question_mark.png')

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        user_nav = self.ids.get('user_nav')
        admin_nav = self.ids.get('admin_nav')

        if app.is_admin:
            if user_nav: user_nav.height, user_nav.opacity, user_nav.disabled = 0, 0, True
            if admin_nav: admin_nav.height, admin_nav.opacity, admin_nav.disabled = '50dp', 1, False
        else:
            if user_nav: user_nav.height, user_nav.opacity, user_nav.disabled = '50dp', 1, False
            if admin_nav: admin_nav.height, admin_nav.opacity, admin_nav.disabled = 0, 0, True
        
        best_seller = self.db_manager.fetch_best_seller()
        
        if best_seller:
            self.best_seller_id = best_seller['id']
            best_seller_button = self.ids.get('best_seller_button')
            best_seller_image = self.ids.get('best_seller_image')
            best_seller_label = self.ids.get('best_seller_label')

            if best_seller_button: best_seller_button.disabled = False

            if best_seller_image:
                img_path_from_db = best_seller['image_path'] if 'image_path' in best_seller.keys() else None
                if img_path_from_db:
                    full_img_path = os.path.abspath(os.path.join(self.assets_path, os.path.basename(img_path_from_db)))
                    if os.path.exists(full_img_path):
                        best_seller_image.source = full_img_path
                    else:
                        best_seller_image.source = self.default_img
                else:
                    best_seller_image.source = self.default_img
            
            if best_seller_label:
                best_seller_label.text = best_seller['name']
        else:
            self.best_seller_id = None
            if self.ids.get('best_seller_button'):
                self.ids.best_seller_button.disabled = True
        
        self.populate_other_products(self.best_seller_id if self.best_seller_id else -1)

    def add_best_seller_to_cart(self):
        if self.best_seller_id is not None:
            app = App.get_running_app()
            app.add_to_cart(self.best_seller_id)
            
            popup = Popup(title="Added to Cart",
                          content=Label(text="Best seller added to your cart!"),
                          size_hint=(0.7, 0.2))
            popup.open()
            
            app.root.current = 'cart'
        else:
            print("No best seller to add.")

    def populate_other_products(self, exclude_id):
        product_list = self.ids.get('product_list')
        if not product_list:
            return
            
        product_list.clear_widgets()
        other_products = self.db_manager.fetch_other_products(exclude_id)
        
        for product in other_products:
            source = self.default_img
            img_path_from_db = product['image_path'] if 'image_path' in product.keys() else None
            
            if img_path_from_db:
                full_img_path = os.path.abspath(os.path.join(self.assets_path, os.path.basename(img_path_from_db)))
                if os.path.exists(full_img_path):
                    source = full_img_path
            
            item = ProductItem(
                product_id=product['id'],
                product_name=product['name'],
                product_price=f"Price: P{product['price']:.2f}",
                image_source=source
            )
            product_list.add_widget(item)
