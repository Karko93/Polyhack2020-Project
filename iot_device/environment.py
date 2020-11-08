import numpy as np
from threading import Thread
from time import sleep

def initialize(sensor_type):
    if sensor_type == 'noise_detector' or sensor_type == 'motion':
        return np.random.rand() > 0.5
    elif sensor_type == 'temperature':
        return 25.0 + np.random.normal(scale=10)
    elif sensor_type == 'humidity':
        return 50.0 + np.random.normal(scale=10)
    elif sensor_type == 'brightness':
        return 50.0 + np.random.normal(scale=10)
    elif sensor_type == 'proximity':
        return np.random.rand() > 0.5
    elif sensor_type == 'distance':
        return 5*np.random.rand()
    elif sensor_type == 'airquality':
        return np.random.rand()
    elif sensor_type == 'antenna':
        return [np.random.rand() for i in range(100)]
    else:
        raise ValueError('Sensor type {} unknown'.format(sensor_type))


class EnvironmentManager(Thread):

    def __init__(self, env):
        Thread.__init__(self)
        self.env = env
        self.daemon = True

    def run(self):
        while True:
            self.env.update_environment()
            sleep(0.1)


class Environment():

    sensors = None # this will be in form {'id1':{'temperature', value, fixed'}}

    def __init__(self, sensors={}):
        """

        :param sensors: dictionary of sensor connected to it (id : type_of_sensor)
        """
        self.sensors = {}
        for sensor, sensor_type in sensors.items():
            self.sensors[sensor] = {'sensor_type': sensor_type,
                                    'value': initialize(sensor_type),
                                    'fixed' : False,
                                   }

    def add_sensor(self, sensor):
        id = sensor.uniq_id
        sensor_type = sensor.sensor_type
        self.sensors[id] = {'sensor_type' : sensor_type,
                            'value' : initialize(sensor_type),
                            'fixed' : False}
        return self

    def update_environment(self):
        for (sensor, information) in self.sensors.items():
            if information['fixed'] is True:
                pass
            else:
                sensor_type = self.sensors[sensor]['sensor_type']
                self.sensors[sensor]['value'] = initialize(sensor_type)
        return self

    def read_value(self, sensor):
        if sensor in self.sensors:
            return self.sensors[sensor]['value']
        else:
            raise Exception('Sensor ' + sensor + ' not present in the list.')
        return self

    def change_val(self, sensor, new_value):
        if sensor in self.sensors:
            self.sensors[sensor]['value'] = new_value
            self.sensors[sensor]['fixed'] = True
        else:
            raise Exception('Sensor ' + sensor + ' not present in the list.')
        return self
