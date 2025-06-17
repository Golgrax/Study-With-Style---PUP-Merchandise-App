from kivy.app import App
from kivy.uix.screenmanager import Screen
from database import DatabaseManager
from widgets.product_item import ProductItem
import os

class HomeScreen(Screen):
    db_manager = DatabaseManager()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    default_img = os.path.join(project_root, 'pup_study_style', 'static', 'assets', 'question_mark.png')

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
            best_seller_image = self.ids.get('best_seller_image')
            best_seller_label = self.ids.get('best_seller_label')
            if best_seller_image:
                img_path_relative = best_seller['image_path'] if 'image_path' in best_seller.keys() else None
                if img_path_relative:
                    img_path_absolute = os.path.abspath(os.path.join(self.project_root, str(img_path_relative).replace('../', '')))
                else:
                    img_path_absolute = None
                if img_path_absolute and os.path.exists(img_path_absolute):
                    best_seller_image.source = img_path_relative
                else:
                    best_seller_image.source = self.default_img
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
            img_path_relative = product['image_path'] if 'image_path' in product.keys() else None
            if img_path_relative:
                img_path_absolute = os.path.abspath(os.path.join(self.project_root, str(img_path_relative).replace('../', '')))
            else:
                img_path_absolute = None
            if img_path_absolute and os.path.exists(img_path_absolute):
                source = img_path_relative
            else:
                source = self.default_img
            
            item = ProductItem(
                product_id=product['id'],
                product_name=product['name'],
                product_price=f"Price: P{product['price']:.2f}",
                image_source=source
            )
            product_list.add_widget(item)
