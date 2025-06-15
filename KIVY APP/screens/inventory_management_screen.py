import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DatabaseManager

class InventoryManagementScreen(Screen):
    db_manager = DatabaseManager()

    def add_item(self):
        item_id = self.ids.item_id_input.text.strip()
        name = self.ids.item_name_input.text.strip()
        quantity = self.ids.quantity_input.text.strip()
        price = self.ids.price_input.text.strip()
        
        if not all([item_id, name, quantity, price]):
            self.show_popup("Error", "All fields are required.")
            return
        
        try:
            quantity_val = int(quantity)
            price_val = float(price)
        except ValueError:
            self.show_popup("Error", "Quantity must be an integer and price must be a number.")
            return

        conn = self.db_manager.get_connection()
        try:
            conn.execute('INSERT INTO inventory (item_id, name, quantity, price) VALUES (?, ?, ?, ?)', (item_id, name, quantity_val, price_val))
            conn.commit()
            self.show_popup("Success", "Item added successfully.")
            self.view_items()
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Item ID already exists.")
        except Exception as e:
            self.show_popup("Error", f"Database error: {e}")
        finally:
            conn.close()

    def view_items(self):
        inventory_list = self.ids.inventory_list
        inventory_list.clear_widgets()
        conn = self.db_manager.get_connection()
        try:
            items = conn.execute('SELECT item_id, name, quantity, price FROM inventory').fetchall()
            for item in items:
                inventory_list.add_widget(Label(text=str(item['item_id'])))
                inventory_list.add_widget(Label(text=item['name']))
                inventory_list.add_widget(Label(text=str(item['quantity'])))
                inventory_list.add_widget(Label(text=f"₱{item['price']:.2f}"))
        except Exception as e:
            inventory_list.add_widget(Label(text=f"Error: {e}"))
        finally:
            conn.close()

    def update_item(self):
        item_id = self.ids.item_id_input.text.strip()
        self.show_popup("Info", "Update functionality not fully implemented in this example.")


    def delete_item(self):
        item_id = self.ids.item_id_input.text.strip()
        self.show_popup("Info", "Delete functionality not fully implemented in this example.")


    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()