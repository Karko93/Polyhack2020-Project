from iot_device.environment import Environment
from iot_device.temperature_sensor import TemperatureSensor
from threading import Thread
from time import sleep


class EnvironmentManager(Thread):

    def __init__(self, env):
        Thread.__init__(self)
        self.env = env

    def run(self):
        while True:
            self.env.update_environment()


info = {'serial' : 0,
        'sensor_type' : 'temp'}

env = Environment({info['serial'] : info['sensor_type']})
sensor = TemperatureSensor(info, env)

clock = EnvironmentManager(env)
clock.start()

print(sensor.data)

sleep(2)
print(sensor.data)
