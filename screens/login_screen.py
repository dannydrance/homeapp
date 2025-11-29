# screens/login_screen.py

from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock

VALID_USERNAME = 'admin'
VALID_PASSWORD = '1234'

# Mock user tuple: (id, username, password, display_name, email, updated_at)
MOCK_USER = ('1', 'admin', '1234', 'Administrator', 'admin@example.com', '2025-01-01')

class LoginScreen(Screen):

    def validate_user(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        # Basic validation
        if not username or not password:
            self.ids.error.text = "⚠ Please enter both username and password"
            return
        app = App.get_running_app()
        try:
            user = None

            # Fake check for now
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                user = MOCK_USER

            if user:
                app.set_user(username)

                display_name = user[3] or username
                self.ids.error.text = ""

                # Welcome toast
                app.toast(f"👋 Welcome back, {display_name}!", color=(0.4, 1, 0.4, 1))

                # Navigate to dashboard
                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'dashboard'), 0.3)
            else:
                self.ids.error.text = "❌ Invalid username or password"

        except Exception as e:
            self.ids.error.text = f"⚠ Login failed: {e}"
            print(f"[Login Error] {e}")
