import threading
import time
import socket


class ConnectionManager:

    def __init__(self, app, local_controller, mqtt_controller):
        self.app = app
        self.local = local_controller
        self.mqtt = mqtt_controller

        self.mode = "unknown"   # "local", "cloud", or "offline"

        # Start background checker thread
        threading.Thread(target=self._connection_monitor, daemon=True).start()

    # -----------------------------------------------------------
    # Check connection status every 5 seconds
    # -----------------------------------------------------------
    def _connection_monitor(self):

        while True:
            try:
                # 1️⃣ Try local IP
                if self._ping_local():
                    if self.mode != "local":
                        print("Mode switched → LOCAL")
                        self.mode = "local"
                    time.sleep(5)
                    continue

                # 2️⃣ Local not available → try MQTT
                if not self.mqtt.connected:
                    self.mqtt.connect_once()

                if self.mqtt.connected:
                    if self.mode != "cloud":
                        print("Mode switched → CLOUD (MQTT)")
                        self.mode = "cloud"
                else:
                    self.mode = "offline"

            except Exception as e:
                print("ConnectionManager Error:", e)

            time.sleep(5)

    # -----------------------------------------------------------
    # Check local IP reachability (NO SPAM)
    # -----------------------------------------------------------
    def _ping_local(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.app.device_ip, 80))
            sock.close()
            return (result == 0)
        except:
            return False
