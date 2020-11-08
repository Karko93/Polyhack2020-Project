from threading import Thread, Lock
from time import sleep
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def plot_data(plot_data_dict, html):
    fig, ax = plt.subplots()
    for key in plot_data_dict:
        x = plot_data_dict[key]['x']
        y = plot_data_dict[key]['y']
        for _y in y:
            ax.plot(x, _y, marker='o', label=key)
    fig.legend(loc='best')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = html + '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    return html

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
                    rule.data.append(self.iot_server.devices[sensor_id].data[reading].iloc[-1])

                # Send jobs based on decision
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
