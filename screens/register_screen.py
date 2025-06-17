from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from database import DatabaseManager
from auth_utils import generate_password_hash

class RegisterScreen(Screen):
    name_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    confirm_password_input = ObjectProperty(None)
    db_manager = DatabaseManager()

    def do_register(self):
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not all([name, email, password, confirm_password]):
            self.show_popup("Error", "All fields are required.")
            return
        if password != confirm_password:
            self.show_popup("Error", "Passwords do not match.")
            return

        if not username:
            username = email

        if self.db_manager.user_exists(username, email):
            self.show_popup("Error", "Username or email already registered.")
            return

        password_hash = generate_password_hash(password)
        success = self.db_manager.insert_user(name, email, username, password_hash)
        
        if success:
            self.show_popup("Success", "Registration successful. Please login.")
            self.manager.current = "login"
        else:
            self.show_popup("Error", "Registration failed. Please try again.")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.3))
        popup.open()
