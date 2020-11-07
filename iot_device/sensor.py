from iot_device.iot_dev import IOT_Device


class Sensor(IOT_Device):
    def __init__(self, id):
        super().__init__(id)
        self.init_at_host()

    def init_at_host(self):
        """Call the host for the first time and pass its object information."""
        message = {'id': self.id, 'ancestors': self.ancestors}
        retval = self._post('recv_json', message)
        if retval == 0:
            self.initialized = True

    def send_to_server(self, data):
        message = {'id': self.id, 'ancestors': self.ancestors, 'data':data}
        retval = self._post('recv_json', message)
        if retval == 0:
            success = True


if __name__ == '__main__':
    dummy_dev = Sensor(id='000000')
    print(dummy_dev.ancestors)
    dummy_dev.send_to_server({'Temperature' : 24.})
