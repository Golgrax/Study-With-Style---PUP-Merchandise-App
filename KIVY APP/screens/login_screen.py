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
        user = self.db_manager.fetch_user(username)
        if user and check_password_hash(user['password_hash'], password):
            app = App.get_running_app()
            app.current_user = username
            app.is_admin = bool(user['is_admin'])
            self.manager.current = "home"
        else:
            popup = Popup(title="Login Failed",
                          content=Label(text="Incorrect username or password."),
                          size_hint=(0.8, 0.3))
            popup.open()

    def logout(self):
        app = App.get_running_app()
        app.current_user = None
        app.is_admin = False
        app.cart = []
        self.manager.current = 'login'