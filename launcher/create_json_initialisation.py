import json 
import numpy as np
import random

filename_sensors = 'initialisation_sensors.json'
filename_actuators = 'initialisation_actuators.json'

sensor_types = ['temperature', 'humidity', 'brightness', 'proximity', 'noise',
                'distance', 'motion', 'airquality', 'distance']

actuator_types = ['SmartLamp', 'SmartDoorLock', 'MotorPosition', 'Heating', 'Sprinkler']


counter_sensors = 0

counter_actuators = 0


def create_sensor():
    global counter_sensors
    newid = counter_sensors
    counter_sensors += 1
    sensor_type = random.choice(sensor_types)
    posx, posy = 30 + np.random.normal(scale=10), 10 + np.random.normal(10)
    dic = {"serial" : newid, "type" : "sensor", "ancestor" : sensor_type,
            "position" : {"x": posx, "y": posy}}
    return dic


def create_actuator():
    global counter_actuators
    newid = counter_actuators + 1000
    counter_actuators += 1
    actuator_type = random.choice(actuator_types)
    posx, posy = 30 + np.random.normal(scale=10), 10 + np.random.normal(10)
    dic = {"serial" : newid, "type" : "Actuator", "ancestor" : actuator_type,
            "position" : {"x": posx, "y": posy}}
    return dic


actuators = [create_actuator() for i in range(10)]
sensors = [create_sensor() for i in range(10)]

with open(filename_sensors, 'w') as f:
    json.dump(sensors, f)

with open(filename_actuators, 'w') as f:
    json.dump(actuators, f)
