import sensor

class TemperatureSensor(sensor.Sensor):

    def __init__(self, jsonFile):
        self.serial = jsonFile['serial']
        self.data = None

    def read_data(self, environment):
        pass

    def parse_data(self, data):
        #some code
        self.data = new_value


