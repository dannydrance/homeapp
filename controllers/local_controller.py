import requests

class LocalController:

    def __init__(self, device_ip):
        self.device_ip = device_ip

    def _url(self, endpoint):
        return f"http://{self.device_ip}/{endpoint}"

    def toggle_light(self):
        try:
            requests.get(self._url("toggleLight"), timeout=2)
            return True
        except:
            return False

    def toggle_fan(self):
        try:
            requests.get(self._url("toggleFan"), timeout=2)
            return True
        except:
            return False

    def is_device_available(self):
        try:
            r = requests.get(self._url("control"), timeout=1)
            return r.status_code == 200
        except:
            return False
