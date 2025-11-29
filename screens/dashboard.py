from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty


class DashboardScreen(Screen):
    light_status = StringProperty("OFF")
    fan_status = StringProperty("OFF")

    def toggle_light(self):
        app = App.get_running_app()

        new_state = "OFF" if self.light_status == "ON" else "ON"

        print(new_state,self.light_status)
        app.toggle_light(new_state)

    def toggle_fan(self):
        app = App.get_running_app()

        new_state = "OFF" if self.fan_status == "ON" else "ON"
        print(new_state)
        app.toggle_fan(new_state)

    def update_ui(self):
        # Called from MQTT ACK parser
        print("UI Updated:", self.light_status, self.fan_status)
