import json
import requests

class IOT_Rules:

    def __init__(self, uniq_id):
        self.uniq_id = uniq_id
        self.sensors = []
        self.actuators = []

    def _post(self, address, message):
        """Wrapper function for POST interaction with the server."""
        s = json.dumps(message)
        host = self.hostname + address
        try:
            return int(requests.post(host, json=s).content)
        except:
            return 1

    def collect_sensor_data(self):
        pass

    def send_actuator_jobs(self):
        pass

if __name__ == '__main__':
    dummy_rul = IOT_Rules(uniq_id='000000')
    print(dummy_rul.send_actuator_jobs())
