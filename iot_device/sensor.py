from iot_device.iot_dev import IOT_Device
from datetime import datetime
from threading import Thread
from time import sleep


class SensorInstantiator(Thread):

    def __init__(self, env, sensors=[], new_sensors=[]):
        """
        :param env: a common environment object
        :param sensors: list of existing sensors
        :param new_sensors: list of new sensors to be added
        """
        Thread.__init__(self)
        self.daemon = True
        self.env = env
        self.sensors = sensors
        self.new_sensors = new_sensors

    def update(self):
        for element in self.new_sensors:
            if element['type'] == 'sensor':
                uniq_id = element['serial']
                position = element['position']
                if element['ancestor'] == 'temperature':
                    self.sensors.append(TemperatureSensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'humidity':
                    self.sensors.append(HumiditySensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'brightness':
                    self.sensors.append(BrightnessSensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'proximity':
                    self.sensors.append(ProximitySensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'noise':
                    self.sensors.append(NoiseSensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'motion':
                    self.sensors.append(MotionSensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'distance':
                    self.sensors.append(DistanceSensor(uniq_id, self.env, position=position))
                elif element['ancestor'] == 'airquality':
                    self.sensors.append(AirQualitySensor(uniq_id, self.env, position=position))
                else:
                    pass
            self.new_sensors.remove(element)
        return self

    def add_sensor(self, sensor):
        """
        :param sensor: dictionary of the same format of the initialisation file.
        :return: self
        """

        self.new_sensors.append(sensor)
        return self

    def run(self):
        while True:
            self.update()
            sleep(1)


class Sensor(IOT_Device):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)

    def send_to_server(self, data):
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'data':data}
        retval = self._post('sensor_com', message)


class PhysicalSensor(Sensor):

    sensor_type = None

    def __init__(self, uniq_id, env):
        super().__init__(uniq_id)
        self._data = None
        self.data_point = None
        self.env = env
        self.env.add_sensor(self)

    def read_data(self):
        self.data_point = self.env.read_value(self.uniq_id)
        return self

    def parse_data(self):
        tsmp = datetime.timestamp(datetime.now())
        self._data = {self.sensor_type: self.data_point, 'timestamp' : tsmp}

    @property
    def data(self):
        self.read_data()
        self.parse_data()
        return self._data


class TemperatureSensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'temperature'
        self.position = position
        super().__init__(uniq_id, env)


class HumiditySensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'humidity'
        self.position = position
        super().__init__(uniq_id, env)


class MotionSensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'motion'
        self.position = position
        super().__init__(uniq_id, env)


class NoiseSensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'noise_detector'
        self.position = position
        super().__init__(uniq_id, env)


class BrightnessSensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'brightness'
        self.position = position
        super().__init__(uniq_id, env)


class ProximitySensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'proximity'
        self.position = position
        super().__init__(uniq_id, env)


class DistanceSensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'distance'
        self.position = position
        super().__init__(uniq_id, env)


class AirQualitySensor(PhysicalSensor):

    def __init__(self, uniq_id, env, position=None):
        self.sensor_type = 'airquality'
        self.position = position
        super().__init__(uniq_id, env)
        



if __name__ == '__main__':
    dummy_dev = Sensor(uniq_id='000001')
    dummy_dev.send_to_server({'Temperature' : 23., 'timestamp': '12:30'})
