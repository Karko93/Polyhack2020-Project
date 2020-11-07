from iot_device.environment import Environment
from iot_device.temperature_sensor import TemperatureSensor
from threading import Thread
from time import sleep


class EnvironmentManager(Thread):

    def __init__(self, env):
        Thread.__init__(self)
        self.env = env
        self.daemon = True

    def run(self):
        while True:
            self.env.update_environment()
            sleep(0.1)

list_of_sensors = {'0'.zfill(6) : 'temp', '1'.zfill(6) : 'temp', '2'.zfill(6) : 'temp'}
# list_of_sensors = {'0'.zfill(6) : 'temp'}

env = Environment(list_of_sensors)
sensors = []

for id in list_of_sensors:
    sensors.append(TemperatureSensor(id, env))

clock = EnvironmentManager(env)
clock.start()

for sensor in sensors:
    data = sensor.data
    print(sensor.uniq_id, data)
    task = sensor.send_to_server(data)
    print(task)
