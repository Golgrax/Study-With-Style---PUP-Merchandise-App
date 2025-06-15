from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class ContactUsScreen(Screen):
    def submit_contact(self):
        name = self.ids.name_input.text.strip()
        email = self.ids.email_input.text.strip()
        message = self.ids.message_input.text.strip()
        
        if not all([name, email, message]):
            popup = Popup(title="Error", content=Label(text="All fields are required."), size_hint=(0.8, 0.3))
            popup.open()
            return
        
        print(f"Contact form submitted:\nName: {name}\nEmail: {email}\nMessage: {message}")
        
        popup = Popup(title="Success", content=Label(text="Message sent successfully."), size_hint=(0.8, 0.3))
        popup.open()
        
        self.ids.name_input.text = ''
        self.ids.email_input.text = ''
        self.ids.message_input.text = ''
