from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from database import DatabaseManager
from auth_utils import check_password_hash

class LoginScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    db_manager = DatabaseManager()

    def do_login(self):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        print(f"--- Attempting login for user: '{username}' ---")
        user = self.db_manager.fetch_user(username)

        if user:
            print(f"User '{username}' found in database.")
            print(f"User data: {dict(user)}") 
            
            password_match = check_password_hash(user['password_hash'], password)
            print(f"Password check result: {password_match}")

            if password_match:
                app = App.get_running_app()
                app.current_user = username
                
                if 'is_admin' in user.keys():
                    app.is_admin = bool(user['is_admin'])
                    print(f"User is_admin flag is: {user['is_admin']} -> Set app.is_admin to {app.is_admin}")
                else:
                    app.is_admin = False
                    print("'is_admin' column not found in user data. Defaulting to non-admin.")

                if app.is_admin:
                    print("Login successful. Navigating to INVENTORY.")
                    self.manager.current = "inventory_management"
                else:
                    print("Login successful. Navigating to HOME.")
                    self.manager.current = "home"
            else:
                print("Login FAILED: Incorrect password.")
                self.show_login_failed_popup()
        else:
            print(f"Login FAILED: User '{username}' not found.")
            self.show_login_failed_popup()

    def show_login_failed_popup(self):
        popup = Popup(title="Login Failed",
                      content=Label(text="Incorrect username or password."),
                      size_hint=(0.8, 0.3))
        popup.open()
