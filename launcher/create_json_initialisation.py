import json 
import numpy as np
import random

number_of_sensors = 60
number_of_actuators = 30


filename_sensors = 'initialisation_sensor.json'
filename_actuators = 'initialisation_actuator.json'

sensor_types = ['temperature', 'humidity', 'brightness', 'proximity', 'noise',
                'distance', 'motion', 'airquality', 'distance']

actuator_types = ['SmartLamp', 'SmartDoorLock', 'MotorPosition', 'Heating', 'Sprinkler']

sensor_kinds = []
actuator_kinds = []

for i in range(number_of_sensors):
    sensor_kinds.append(sensor_types[i % len(sensor_types)])

for i in range(number_of_actuators):
    actuator_kinds.append(actuator_types[i % len(actuator_types)])



counter_sensors = 0

counter_actuators = 0


def create_sensor(sensor_type):
    global counter_sensors
    newid = counter_sensors
    counter_sensors += 1
    posx, posy = 47.40667 + np.random.normal(scale=1e-2), 8.55 + np.random.normal(scale=1e-2)
    dic = {"serial" : str(newid).zfill(5), "type" : "sensor", "ancestor" : sensor_type,
            "position" : {"x": posx, "y": posy}}
    return dic


def create_actuator(actuator_type):
    global counter_actuators
    newid = counter_actuators + 10000
    counter_actuators += 1
    posx, posy = 47.40667 + np.random.normal(scale=1e-2), 8.55 + np.random.normal(scale=1e-2)
    dic = {"serial" : str(newid).zfill(5), "type" : "Actuator", "ancestor" : actuator_type,
            "position" : {"x": posx, "y": posy}}
    return dic


actuators = [create_actuator(actuator_kinds[i]) for i in range(number_of_actuators)]
sensors = [create_sensor(sensor_kinds[i]) for i in range(number_of_sensors)]

with open(filename_sensors, 'w') as f:
    json.dump(sensors, f, indent=4)

with open(filename_actuators, 'w') as f:
    json.dump(actuators, f, indent=4)
