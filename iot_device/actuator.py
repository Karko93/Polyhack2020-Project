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

    def check_for_open_jobs(self):
        pass


class SmartDoorLock(Actuator):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.isDoorOpen = True  # State if door is open
        self.openJobs = {}

    def update_status(self):
        if self.openJobs:
            self.isDoorOpen = self.openJobs['openDoor']
            self.openJobs = {}



class MotorPosition(Actuator):
    def __init__(self, uniq_id, position_x = 0, position_y = 0):
        super().__init__(uniq_id)
        self.position_x = position_x # heating switched on
        self.position_y = position_y
        self.openJobs = {}

    def update_status(self):
        if self.openJobs:
            self.position_x = self.openJobs['position_x']
            self.position_y = self.openJobs['position_y']
            self.openJobs = {}


class SmartLamp(Actuator):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.intensity = 0  # Intensity of the lamp
        self.openJobs = {}

    # Check if there are open jobs and update the intensity according to the las value
    def update_status(self):
        if self.openJobs:
            self.intensity = self.openJobs['intensity']
            self.openJobs = {}


class Heating(Actuator):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.heating_on = 0  # heating switched on
        self.openJobs = {}

    def update_status(self):
        if self.openJobs:
            self.heating_on = self.openJobs['heating_on']
            self.openJobs = {}

class Sprinkler(Actuator):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.water_running = 0  # sprinkler switched on
        self.openJobs = {}

    def update_status(self):
        if self.openJobs:
            self.water_running = self.openJobs['water_running']
            self.openJobs = {}

if __name__ == '__main__':
    dummy_dev = Actuator(uniq_id='000100')
    print(dummy_dev.ancestors)
