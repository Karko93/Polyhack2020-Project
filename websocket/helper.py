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
                # print(rule)
                # Check if all Sensors are existing
                ret_val = self.check_if_exist(rule.sensor_ids)
                if ret_val == 1:
                    continue
                else:
                    # print('all sensors there')
                    # Check if all Actuators are existing
                    ret_val = self.check_if_exist(rule.actuator_ids)
                    if ret_val == 1:
                        continue
                    # print('all actuators there')

                # Collect Sensor data
                rule.data = []
                for sensor_id, reading in zip(rule.sensor_ids, rule.sensor_reading):
                    print(self.iot_server.devices[sensor_id].data)
                    rule.data.append(self.iot_server.devices[sensor_id].data[reading].iloc[-1])

                # Send jobs based on decision
                print(rule.rule_decision())
                if rule.rule_decision():
                    actuator_value = rule.actuator_value_True
                elif rule.actuator_value_False is not None:
                    actuator_value = rule.actuator_value_False
                else: continue
                n = len(rule.actuator_ids)
                for actuator_id, output, value in zip(rule.actuator_ids,
                                               rule.actuator_output * n,
                                               actuator_value * n):
                    self.iot_server.devices[actuator_id].jobs = {output: value}
                rule.data = []

            sleep(5)
