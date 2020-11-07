from iot_device.iot_dev import IOT_Device


class Sensor(IOT_Device):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)

    def send_to_server(self, data):
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'data':data}
        retval = self._post('sensor_com', message)


if __name__ == '__main__':
    dummy_dev = Sensor(uniq_id='000001')
    dummy_dev.send_to_server({'Temperature' : 23., 'timestamp': '12:30'})
