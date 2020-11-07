from iot_device.sensor import Sensor

class TemperatureSensor(Sensor):

    def __init__(self, jsonFile):
        self.serial = jsonFile['serial']
        self.data = None
        self.data_point = None

    def read_data(self, env):
        self.data_point = env.read_value(self.serial)
        return self

    def parse_data(self):
        #some code
        self.data = {'temperature': self.data_point}


