import numpy as np

def initialize_temperature():
    return 25.0 + np.random.normal(scale=10)

def initialize_humidity():
    return 50.0 + np.random.normal(scale=10)

def initialize_motion_sensor():
    return np.random.rand() > 0.5

def initialize_noise_detector():
    return np.random.rand() > 0.5

def initialize(sensor_type):
    if sensor_type == 'noise_detector' or sensor_type == 'motion_sensor':
        return np.random.rand() > 0.5
    elif sensor_type == 'temperature':
        return 25.0 + np.random.normal(scale=10)
    elif sensor_type == 'humidity':
        return 50.0 + np.random.normal(scale=10)
    elif sensor_type == 'brightness':
        return 50.0 + np.random.normal(scale=10)
    elif sensor_type == 'proximity_sensor':
        return np.random.rand() > 0.5


class Environment():

    sensors = {} # this will be in form {'id1':{'temperature', value, fixed'}}

    def __init__(self, sensors=None):
        """

        :param sensors: dictionary of sensor connected to it (id : type_of_sensor)
        """
        if sensors is not None:
            for (sensor, sensor_type) in sensors.items():
                if sensor_type in 'temperature':
                    self.sensors[sensor] = {'sensor_type' : 'temperature',
                                            'value' : initialize_temperature(),
                                            'fixed' : False}
                elif sensor_type in 'humidity':
                    self.sensors[sensor] = {'sensor_type' : 'humidity',
                                            'value' : initialize_humidity(),
                                            'fixed' : False}
                elif sensor_type in 'motion_sensor':
                    self.sensors[sensor] = {'sensor_type' : 'motion_sensor',
                                            'value' : initialize_motion_sensor(),
                                            'fixed' : False}
                elif sensor_type in 'smart_noise_detector':
                    self.sensors[sensor] = {'sensor_type' : 'noise_detector',
                                            'value': initialize_noise_detector(),
                                            'fixed' : False}
                else:
                    raise Exception('Sensor type unknown.')

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
