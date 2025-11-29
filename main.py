from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

from screens.login_screen import LoginScreen
from screens.dashboard import DashboardScreen

# Controllers
from controllers.local_controller import LocalController
from controllers.mqtt_controller import MQTTController
from controllers.connection_manager import ConnectionManager

# Load KV files
Builder.load_file("kv/login.kv")
Builder.load_file("kv/dashboard.kv")


class HomeLightApp(App):

    def build(self):

        # ----------------------------------------------------------
        # DEVICE CONFIG (MATCHING ESP8266 FIRMWARE)
        # ----------------------------------------------------------
        self.device_serial = "ESP1234"   # SAME SERIAL AS ESP8266
        self.device_ip     = "192.168.1.50"   # LOCAL STATIC IP

        # ----------------------------------------------------------
        # MQTT CONFIG (MATCHING YOUR ESP8266)
        # ----------------------------------------------------------
        self.mqtt_server   = "bffac683e63348f5b429862109209547.s1.eu.hivemq.cloud"
        self.mqtt_port     = 8883
        self.mqtt_user     = "hivemq.webclient.1762324468600"
        self.mqtt_password = "Cv;*bFcq>y8KT237.DhJ"

        # ----------------------------------------------------------
        # CREATE CONTROLLERS
        # ----------------------------------------------------------
        self.local = LocalController(self.device_ip)

        self.mqtt = MQTTController(
            app=self,
            server=self.mqtt_server,
            port=self.mqtt_port,
            user=self.mqtt_user,
            password=self.mqtt_password,
            device_serial=self.device_serial
        )

        self.conn = ConnectionManager(self, self.local, self.mqtt)

        # ----------------------------------------------------------
        # SCREEN MANAGER
        # ----------------------------------------------------------
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(DashboardScreen(name="dashboard"))

        return self.sm

    # ----------------------------------------------------------
    # USER
    # ----------------------------------------------------------
    def set_user(self, username):
        self.current_user = username

    # ----------------------------------------------------------
    # TOAST MESSAGE
    # ----------------------------------------------------------
    def toast(self, message, color=(1, 1, 1, 1), duration=2):
        view = ModalView(size_hint=(None, None), size=(300, 50),
                         background_color=(0, 0, 0, 0.8))
        lbl = Label(text=message, color=color)
        view.add_widget(lbl)
        view.open()
        Clock.schedule_once(lambda dt: view.dismiss(), duration)

    # ----------------------------------------------------------
    # DEVICE COMMANDS (CALLED BY DASHBOARD)
    # ----------------------------------------------------------
    def toggle_light(self, target_state):
        """
        target_state = "ON" or "OFF"
        """
        if self.conn.mode == "local":
            self.local.toggle_light()
        else:
            self.mqtt.send_light(target_state)

    def toggle_fan(self, target_state):
        if self.conn.mode == "local":
            self.local.toggle_fan()
        else:
            self.mqtt.send_fan(target_state)

    # ----------------------------------------------------------
    # MQTT ACK RECEIVED
    # ----------------------------------------------------------
    @mainthread
    def update_status_from_ack(self, msg):
        """
        ESP sends:  Light:ON,Fan:OFF
        """
        try:
            parts = msg.split(",")
            light = parts[0].split(":")[1]
            fan = parts[1].split(":")[1]

            print('mess', light, fan)

            dash = self.sm.get_screen("dashboard")
            dash.light_status = light
            dash.fan_status = fan
            dash.update_ui()

        except Exception as e:
            print("ACK Parse Error:", e)


if __name__ == "__main__":
    HomeLightApp().run()
