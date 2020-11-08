import pandas as pd
from threading import Thread, Lock
from time import sleep


def html_table(table):
    return pd.DataFrame(data=table).to_html()


class BackgroundWorker(Thread):
    def __init__(self, iot_server):
        Thread.__init__(self)
        self.iot_server = iot_server
        self.daemon = True
        self.name = self.__class__.__name__

    def check_if_exist(self, all_ids):
        for unq_id in all_ids:
            if unq_id not in self.iot_server.devices:
                return 1
        return 0

    def run(self):
        while True:
            rules = self.iot_server.rules
            for rule in rules:
                # Check if all Sensors are existing
                ret_val = self.check_if_exist(rule.sensor_ids)
                if ret_val == 1:
                    continue
                else:
                    # Check if all Actuators are existing
                    ret_val = self.check_if_exist(rule.actuator_ids)
                    if ret_val == 1:
                        continue

                # Collect Sensor data
                rule.data = []
                for sensor_id, reading in zip(rule.sensor_ids, rule.sensor_reading):
                    rule.data.append(self.iot_server.devices[sensor_id].data[reading].iloc[-1])

                # Send jobs based on decision
                if rule.rule_decision():
                    for actuator_id, output in zip(rule.actuator_ids, rule.actuator_output):
                        self.iot_server.devices[actuator_id].jobs = output
                rule.data = []

            sleep(5)
