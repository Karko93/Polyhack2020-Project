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
"""
list_of_sensors = [{
  "serial": str(1).zfill(2),
  "type": "sensor",
  "ancestor": "brightness",
  "position":{
    "x": 47.410847,
    "y":  8.537878}
}, {
  "serial": str(2).zfill(2),
  "type": "sensor",
  "ancestor": "temperature",
  "position":{
    "x": 47.410847,
    "y":  8.537878}
}, {
  "serial": str(3).zfill(2),
  "type": "sensor",
  "ancestor": "proximity",
  "position":{
    "x": 47.410847,
    "y":  8.537878}
}, {
  "serial": str(4).zfill(2),
  "type": "sensor",
  "ancestor": "noise",
  "position":{
    "x": 46.410847,
    "y":  7.537178}
}, {
  "serial": str(5).zfill(2),
  "type": "sensor",
  "ancestor": "distance",
  "position":{
    "x": 47.410847,
    "y":  8.537878}
}, {
  "serial": str(6).zfill(2),
  "type": "sensor",
  "ancestor": "motion",
  "position":{
    "x": 47.410847,
    "y":  8.537878}
}, {
  "serial": str(7).zfill(2),
  "type": "sensor",
  "ancestor": "humidity",
  "position":{
    "x": 37.410847,
    "y":  10.137878}
},{
        "serial": str(8).zfill(2),
        "type": "sensor",
        "ancestor": "humidity",
        "position": {
            "x": 37.410847,
            "y": 10.137878}
    }, {
        "serial": str(9).zfill(2),
        "type": "sensor",
        "ancestor": "airquality",
        "position": {
            "x": 37.410847,
            "y": 10.137878}
    }
]"""

for new_element in list_of_sensors:
    sensor_parser.add_sensor(new_element)

"""
for id in range(5):
    new_sensors.append(TemperatureSensor(str(counter).zfill(6), env))
    counter += 1

for id in range(5):
    new_sensors.append(HumiditySensor(str(counter).zfill(6), env))
    counter += 1

for id in range(5):
    new_sensors.append(NoiseSensor(str(counter).zfill(6), env))
    counter += 1

for id in range(5):
    new_sensors.append(MotionSensor(str(counter).zfill(6), env))
    counter += 1

for id in range(10):
    new_sensors.append(BrightnessSensor(str(counter).zfill(6), env))
    counter += 1


for id in range(1):
    new_sensors.append(Antenna(str(counter).zfill(6), env))
    counter += 1"""

clock = EnvironmentManager(env)
clock.start()

sleep(0.5)


while True:
    for sensor in sensor_parser.sensors:
        data = sensor.data
        print(sensor.uniq_id, data)
        sensor.send_to_server(data)
    sleep(1)

