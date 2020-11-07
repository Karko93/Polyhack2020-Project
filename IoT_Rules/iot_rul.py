import json
import requests
from websocket.server import iot_server


class IOT_Rules:

    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        self.uniq_id = uniq_id
        self.sensor_ids = sensor_id_list
        self.actuator_ids = actuator_id_list
        self.data = []


    def collect_sensor_data(self):
        for sensor_id in self.sensor_ids:
            if sensor_id in iot_server.sensors:
                self.data.append(iot_server.sensors[sensor_id].data.iloc[-1])

    def rule_decision(self):
        pass

    def send_actuator_jobs(self):
        decisions = self.rule_decision()
        return (self.actuator_ids, decisions)

if __name__ == '__main__':
    dummy_rul = IOT_Rules(uniq_id='000000')
    print(dummy_rul.send_actuator_jobs())
