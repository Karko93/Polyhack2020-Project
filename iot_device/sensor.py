from iot_device.iot_dev import IOT_Device


class Sensor(IOT_Device):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        # self.init_at_host()

    # def init_at_host(self):
    #     """Call the host for the first time and pass its object information."""
    #     message = {'id': self.uniq_id, 'ancestors': self.ancestors}
    #     retval = self._post('recv_json', message)
    #     if retval == 0:
    #         self.initialized = True

    def send_to_server(self, data):
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'data':data}
        retval = self._post('recv_json', message)
        if retval == 0:
            success = True


if __name__ == '__main__':
    dummy_dev = Sensor(uniq_id='000001')
    print(dummy_dev.ancestors)
    dummy_dev.send_to_server({'Temperature' : 23., 'timestamp': '12:30'})
    print(globals()['Sensor'])
