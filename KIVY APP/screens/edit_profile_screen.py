from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty
from database import DatabaseManager

class EditProfileScreen(Screen):
    username = StringProperty('')
    db_manager = DatabaseManager()

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.username = getattr(app, 'current_user', '')
        profile = self.db_manager.fetch_profile(self.username)

        if profile:
            self.ids.name_input.text = profile.get('name', '')
            self.ids.address1_input.text = profile.get('address1', '')
            self.ids.contact1_input.text = profile.get('contact1', '')
            self.ids.address2_input.text = profile.get('address2', '')
            self.ids.contact2_input.text = profile.get('contact2', '')
        else:
            for field_id in ['name_input', 'address1_input', 'contact1_input', 'address2_input', 'contact2_input']:
                self.ids[field_id].text = ''

    def save_profile(self):
        name = self.ids.name_input.text.strip()
        address1 = self.ids.address1_input.text.strip()
        contact1 = self.ids.contact1_input.text.strip()
        address2 = self.ids.address2_input.text.strip()
        contact2 = self.ids.contact2_input.text.strip()

        success = self.db_manager.update_profile(self.username, name, address1, contact1, address2, contact2)
        
        if success:
            content = "Profile updated successfully."
            popup = Popup(title="Profile Update", content=Label(text=content), size_hint=(0.8, 0.3))
            popup.open()
            self.manager.current = 'profile'
        else:
            content = "Failed to update profile."
            popup = Popup(title="Error", content=Label(text=content), size_hint=(0.8, 0.3))
            popup.open()
