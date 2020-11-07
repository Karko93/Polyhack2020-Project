from iot_device.iot_dev import IOT_Device


class Actuator(IOT_Device):
    jobs = {}
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.init_at_host()

    def init_at_host(self):
        """Call the host for the first time and pass its object information."""
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'jobs': self.jobs}
        retval = self._post('actuator_com', message)


if __name__ == '__main__':
    dummy_dev = Actuator(uniq_id='000100')
    print(dummy_dev.ancestors)
