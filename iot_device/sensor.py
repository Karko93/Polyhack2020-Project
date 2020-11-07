from iot_device.iot_dev import IOT_Device
from datetime import datetime


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

    def __init__(self, uniq_id, env):
        self.sensor_type = 'temperature'
        super().__init__(uniq_id, env)


class HumiditySensor(PhysicalSensor):

    def __init__(self, uniq_id, env):
        self.sensor_type = 'humidity'
        super().__init__(uniq_id, env)


class MotionSensor(PhysicalSensor):

    def __init__(self, uniq_id, env):
        self.sensor_type = 'motion_sensor'
        super().__init__(uniq_id, env)


class NoiseSensor(PhysicalSensor):

    def __init__(self, uniq_id, env):
        self.sensor_type = 'noise_detector'
        super().__init__(uniq_id, env)


class BrightnessSensor(PhysicalSensor):

    def __init__(self, uniq_id, env):
        self.sensor_type = 'brightness_sensor'
        super().__init__(uniq_id, env)


if __name__ == '__main__':
    dummy_dev = Sensor(uniq_id='000001')
    dummy_dev.send_to_server({'Temperature' : 23., 'timestamp': '12:30'})
