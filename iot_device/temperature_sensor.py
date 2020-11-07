from iot_device.sensor import Sensor

class TemperatureSensor(Sensor):

    def __init__(self, jsonFile, env):
        self.serial = jsonFile['serial']
        self._data = None
        self.data_point = None
        self.env = env

    def read_data(self):
        self.data_point = self.env.read_value(self.serial)
        return self

    def parse_data(self):
        self._data = {'temperature': self.data_point}

    @property
    def data(self):
        self.read_data()
        self.parse_data()
        return self._data
