import paho.mqtt.client as mqtt
import threading
import ssl


class MQTTController:

    def __init__(self, app, server, port, user, password, device_serial):
        self.app = app
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.device_serial = device_serial

        self.connected = False

        self.client = mqtt.Client()
        self.client.username_pw_set(self.user, self.password)

        # TLS REQUIRED by HiveMQ Cloud
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    # -------------------------------------------------------
    # Connect ONCE (NOT IN A LOOP)
    # -------------------------------------------------------
    def connect_once(self):
        if self.connected:
            return

        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        print("MQTT: Connecting…")

        try:
            self.client.connect(self.server, self.port, keepalive=30)
            self.client.loop_start()
        except Exception as e:
            print("MQTT Connect Failed:", e)

    # -------------------------------------------------------
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT Connected OK")
            self.connected = True

            topic = f"{self.device_serial}/ack"
            client.subscribe(topic)
            print("Subscribed to:", topic)
        else:
            print("MQTT Connection failed. RC:", rc)

    # -------------------------------------------------------
    def _on_message(self, client, userdata, msg):
        ack = msg.payload.decode()
        print("ACK Received:", ack)
        self.app.update_status_from_ack(ack)

    # -------------------------------------------------------
    # Send Commands
    # -------------------------------------------------------
    def send_light(self, state):
        if not self.connected:
            print("MQTT not connected.")
            return
        self.client.publish(f"{self.device_serial}/light/set", state)
        print('send publication to', f"{self.device_serial}/light/set", state)

    def send_fan(self, state):
        if not self.connected:
            print("MQTT not connected.")
            return
        self.client.publish(f"{self.device_serial}/fan/set", state)
        print('send publication to', f"{self.device_serial}/fan/set", state)
