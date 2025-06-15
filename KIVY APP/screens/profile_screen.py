from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from database import DatabaseManager

class ProfileScreen(Screen):
    username = StringProperty('')
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.username = getattr(app, 'current_user', '')
        
        if not all(k in self.ids for k in ['name_label', 'address1_label', 'contact1_label', 'address2_label', 'contact2_label']):
            return

        profile = self.db_manager.fetch_profile(self.username)
        if profile:
            self.ids.name_label.text = f"Name: {profile.get('name') or 'Not set'}"
            self.ids.address1_label.text = profile.get('address1') or 'Not set'
            self.ids.contact1_label.text = f"Contact: {profile.get('contact1') or 'Not set'}"
            self.ids.address2_label.text = profile.get('address2') or 'Not set'
            self.ids.contact2_label.text = f"Contact: {profile.get('contact2') or 'Not set'}"
        else:
            self.ids.name_label.text = "Name: Not set"
            self.ids.address1_label.text = 'Not set'
            self.ids.contact1_label.text = 'Contact: Not set'
            self.ids.address2_label.text = 'Not set'
            self.ids.contact2_label.text = 'Contact: Not set'

    def logout(self):
        app = App.get_running_app()
        app.current_user = None
        app.cart = []
        self.manager.current = 'login'