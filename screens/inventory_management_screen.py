import sqlite3
import os
import shutil
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from database import DatabaseManager

class InventoryManagementScreen(Screen):
    db_manager = DatabaseManager()
    selected_image_path = ""
    assets_folder = os.path.join(os.path.dirname(__file__), '..', 'pup_study_style', 'static', 'assets')
    
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app.is_admin:
            self.manager.current = 'login'
            Popup(title="Access Denied",
                  content=Label(text="You must be an admin to access this page."),
                  size_hint=(0.8, 0.3)).open()
            return
        self.view_items()
        self.clear_inputs()

    def add_item(self):
        name = self.ids.item_name_input.text.strip()
        quantity_str = self.ids.quantity_input.text.strip()
        price_str = self.ids.price_input.text.strip()
        
        if not all([name, quantity_str, price_str]):
            self.show_popup("Error", "Name, Quantity, and Price are required.")
            return
        
        try:
            quantity = int(quantity_str)
            price = float(price_str)
        except ValueError:
            self.show_popup("Error", "Quantity must be an integer and price must be a number.")
            return

        conn = self.db_manager.get_connection()
        try:
            conn.execute('INSERT INTO products (name, stock_quantity, price, image_path) VALUES (?, ?, ?, ?)', 
                         (name, quantity, price, self.selected_image_path))
            conn.commit()
            self.show_popup("Success", "Item added successfully.")
            self.view_items()
            self.clear_inputs()
        except sqlite3.Error as e:
            self.show_popup("Error", f"Database error: {e}")
        finally:
            conn.close()
            
    def update_item(self):
        item_id_str = self.ids.item_id_input.text.strip()
        name = self.ids.item_name_input.text.strip()
        quantity_str = self.ids.quantity_input.text.strip()
        price_str = self.ids.price_input.text.strip()

        if not item_id_str:
            self.show_popup("Error", "Please load an item first.")
            return

        try:
            item_id = int(item_id_str)
            quantity = int(quantity_str)
            price = float(price_str)
        except ValueError:
            self.show_popup("Error", "Invalid ID, Quantity, or Price format.")
            return
        
        conn = self.db_manager.get_connection()
        try:
            if self.selected_image_path:
                image_to_update = self.selected_image_path
            else:
                old_product = self.db_manager.fetch_product_by_id(item_id)
                image_to_update = old_product['image_path'] if old_product and 'image_path' in old_product.keys() else ''
            
            cursor = conn.execute('UPDATE products SET name = ?, stock_quantity = ?, price = ?, image_path = ? WHERE id = ?',
                               (name, quantity, price, image_to_update, item_id))
            if cursor.rowcount == 0:
                self.show_popup("Error", "Item ID not found.")
            else:
                conn.commit()
                self.show_popup("Success", "Item updated successfully.")
                self.view_items()
                self.clear_inputs()
        except sqlite3.Error as e:
            self.show_popup("Error", f"Database error: {e}")
        finally:
            conn.close()

    def delete_item(self):
        item_id_str = self.ids.item_id_input.text.strip()
        if not item_id_str:
            self.show_popup("Error", "Item ID is required to delete.")
            return
            
        conn = self.db_manager.get_connection()
        try:
            item_id = int(item_id_str)
            cursor = conn.execute('DELETE FROM products WHERE id = ?', (item_id,))
            if cursor.rowcount == 0:
                self.show_popup("Error", "Item ID not found.")
            else:
                conn.commit()
                self.show_popup("Success", "Item deleted successfully.")
                self.view_items()
                self.clear_inputs()
        except ValueError:
            self.show_popup("Error", "Item ID must be a number.")
        except sqlite3.Error as e:
            self.show_popup("Error", f"Database error: {e}")
        finally:
            conn.close()

    def load_item_for_update(self):
        item_id_str = self.ids.item_id_input.text.strip()
        if not item_id_str:
            self.show_popup("Error", "Please enter an Item ID to load.")
            return
        
        try:
            item_id = int(item_id_str)
            product = self.db_manager.fetch_product_by_id(item_id)
            if product:
                self.ids.item_name_input.text = product['name']
                self.ids.quantity_input.text = str(product['stock_quantity'])
                self.ids.price_input.text = str(product['price'])
                self.ids.image_path_label.text = product['image_path'] if 'image_path' in product.keys() else 'No image'
                self.selected_image_path = ""
            else:
                self.show_popup("Not Found", f"No product with ID {item_id}.")
                self.clear_inputs(keep_id=True)
        except ValueError:
            self.show_popup("Error", "Item ID must be a number.")

    def view_items(self):
        inventory_list = self.ids.inventory_list
        inventory_list.clear_widgets()
        conn = self.db_manager.get_connection()
        try:
            items = conn.execute('SELECT id, name, stock_quantity, price FROM products').fetchall()
            if not items:
                inventory_list.add_widget(Label(text="No products in inventory.", color=(0.2,0.2,0.2,1)))
                return
                
            for item in items:
                inventory_list.add_widget(Label(text=str(item['id']), color=(0.2,0.2,0.2,1)))
                inventory_list.add_widget(Label(text=item['name'], color=(0.2,0.2,0.2,1)))
                inventory_list.add_widget(Label(text=str(item['stock_quantity']), color=(0.2,0.2,0.2,1)))
                inventory_list.add_widget(Label(text=f"P{item['price']:.2f}", color=(0.2,0.2,0.2,1)))
        except sqlite3.Error as e:
            inventory_list.add_widget(Label(text=f"Error: {e}", color=(0.8,0,0,1)))
        finally:
            conn.close()
            
    def open_file_chooser(self):
        content = BoxLayout(orientation='vertical')
        home_dir = os.path.expanduser('~')
        file_chooser = FileChooserListView(path=home_dir)
        content.add_widget(file_chooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height='44dp')
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        popup = Popup(title="Choose an image", content=content, size_hint=(0.9, 0.9))
        
        def select_file(instance):
            if file_chooser.selection:
                source_path = file_chooser.selection[0]
                filename = os.path.basename(source_path)
                destination_path = os.path.join(self.assets_folder, filename)

                if not os.path.exists(self.assets_folder):
                    os.makedirs(self.assets_folder)

                shutil.copy(source_path, destination_path)
                
                self.selected_image_path = os.path.join('..', 'pup_study_style', 'static', 'assets', filename).replace("\\", "/")
                self.ids.image_path_label.text = filename
                popup.dismiss()

        select_btn.bind(on_release=select_file)
        cancel_btn.bind(on_release=popup.dismiss)
        popup.open()

    def clear_inputs(self, keep_id=False):
        if not keep_id:
            self.ids.item_id_input.text = ""
        self.ids.item_name_input.text = ""
        self.ids.quantity_input.text = ""
        self.ids.price_input.text = ""
        self.ids.image_path_label.text = "No image selected"
        self.selected_image_path = ""

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

    def logout(self):
        app = App.get_running_app()
        app.current_user = None
        app.is_admin = False
        self.manager.current = 'login'
