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

sensor = TemperatureSensor(info)
env = Environment({info['serial'] : info['sensor_type']})

clock = EnvironmentManager(env)
clock.start()

sensor.read_data(env).parse_data()
print(sensor.data)

sleep(2)
sensor.read_data(env).parse_data()
print(sensor.data)
