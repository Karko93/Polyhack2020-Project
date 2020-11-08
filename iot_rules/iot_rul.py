import json
import requests
# from websocket.server import iot_server

class IOT_Rules:
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        self.uniq_id = uniq_id
        self.sensor_ids = sensor_id_list
        self.actuator_ids = actuator_id_list
        self.data = []
        self.sensor_reading = []
        self.actuator_output = []

    def rule_decision(self):
        pass


class SmartStreetLight(IOT_Rules):
    def __init__(self,uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id, sensor_id_list, actuator_id_list)
        self.sensor_reading = ['motion_sensor', 'noise_detector']
        self.actuator_output = ['switch']

    def rule_decision(self):
        # Switches the light on if both of the sensors (motion and noise) detect something
        print(self.data)
        return (self.data[0] and self.data[1])

if __name__ == '__main__':
    dummy_rul = IOT_Rules(uniq_id='000000')
    print(dummy_rul.send_actuator_jobs())
