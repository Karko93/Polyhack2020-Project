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
        if retval == 0:
            self.initialized = True

    def check_for_open_jobs(self):
        pass


class SmartDoorLock(Actuator):

    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.isDoorOpen = True  # State if door is open
        self.openJobs = []

    def update_status(self):
        if self.openJobs:
            self.isDoorOpen = self.openJobs[0]



class SmartLamp(Actuator):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.intensity = 0  # Intensity of the lamp
        self.openJobs = []

    def update_status(self):
        if self.openJobs:
            self.intensity = self.openJobs[-1]





if __name__ == '__main__':
    dummy_dev = Actuator(uniq_id='000000')
    print(dummy_dev.ancestors)
