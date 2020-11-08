from iot_device.environment import Environment, EnvironmentManager
from iot_device.sensor import *
from time import sleep
#from antenna_actuator_sensor import Antenna

import json

filename = 'Documents/initialisation.json'

with open(filename) as initialisation_file:
    list_of_sensors = json.load(initialisation_file)

sensors = []
new_sensors = []

env = Environment()
sensor_parser = SensorInstantiator(env, sensors=sensors, new_sensors=new_sensors)
sensor_parser.start()

counter = 0

for new_element in list_of_sensors:
    sensor_parser.add_sensor(new_element)


clock = EnvironmentManager(env)
clock.start()

sleep(0.5)


while True:
    for sensor in sensor_parser.sensors:
        data = sensor.data
        print(sensor.uniq_id, data)
        sensor.send_to_server(data)
    sleep(1)

