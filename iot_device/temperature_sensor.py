from iot_device.sensor import Sensor
from datetime import datetime


class TemperatureSensor(Sensor):

    def __init__(self, uniq_id, env):
        super().__init__(uniq_id)
        self._data = None
        self.data_point = None
        self.env = env

    def read_data(self):
        self.data_point = self.env.read_value(self.uniq_id)
        return self

    def parse_data(self):
        tsmp = datetime.timestamp(datetime.now())
        self._data = {'Temperature': self.data_point, 'timestamp' : tsmp}

    @property
    def data(self):
        self.read_data()
        self.parse_data()
        return self._data

if __name__ == '__main__':
    dummy_dev = TemperatureSensor(uniq_id='000001')
    dummy_dev.send_to_server({'Temperature' : 23., 'timestamp': '12:30'})
