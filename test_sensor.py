from iot_device.environment import Environment, EnvironmentManager
from iot_device.sensor import *
import iot_device.actuator
from time import sleep
#from antenna_actuator_sensor import Antenna

import json

filename_sensors = 'Documents/initialisation_sensor.json'
filename_actuators = 'Documents/initialisation_actuator.json'

with open(filename_sensors) as initialisation_file:
    list_of_sensors = json.load(initialisation_file)
with open(filename_actuators) as initialisation_file:
    list_of_actuators = json.load(initialisation_file)

actuators = [getattr(iot_device.actuator, act['ancestor'])(act['serial'], act['position']) for act in list_of_actuators]
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
    for actuator in actuators:
        actuator.update_status()
    sleep(1)

