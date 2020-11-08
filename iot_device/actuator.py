from iot_device.iot_dev import IOT_Device
from datetime import datetime
import json

class Actuator(IOT_Device):
    data = None
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.actuator_type = None
        self.status = None

    def send_to_server(self):
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'data': self.data}
        retval = self._post('actuator_com', message)
        return retval



class SmartDoorLock(Actuator):
    def __init__(self, uniq_id,position=None):
        super().__init__(uniq_id)
        self.actuator_type = "doorlock"
        self.isDoorOpen = True  # State if door is open
        self.openJobs = {}
        self.status = self.isDoorOpen
        self.position = position

    def update_status(self):
        if self.openJobs:
            self.isDoorOpen = self.openJobs['openDoor']
            self.status = self.isDoorOpen
            self.openJobs = {}



class MotorPosition(Actuator):
    def __init__(self, uniq_id, position_x = 0, position_y = 0,position=None):
        super().__init__(uniq_id)
        self.actuator_type = "motorposition"
        self.position_x = position_x # heating switched on
        self.position_y = position_y
        self.status = [self.position_x, self.position_y]
        self.openJobs = {}
        self.position = position

    def update_status(self):
        if self.openJobs:
            self.position_x = self.openJobs['position_x']
            self.position_y = self.openJobs['position_y']
            self.status = [self.position_x, self.position_y]
            self.openJobs = {}


class SmartLamp(Actuator):
    def __init__(self, uniq_id,position=None):
        super().__init__(uniq_id)
        self.data = {'intensity': 0}
        self.position = position

    # Check if there are open jobs and update the intensity according to the las value
    def update_status(self):
        try:
            retval = json.loads(self.send_to_server())
        except:
            return
        if not retval:
            return
        else:
            for job in retval:
                if job == 'switch':
                    self.data['intensity'] = retval[job]


class Heating(Actuator):
    def __init__(self, uniq_id,position=None):
        super().__init__(uniq_id)
        self.actuator_type = "heating"
        self.heating_on = 0  # heating switched on
        self.status = self.heating_on
        self.openJobs = {}
        self.position = position

    def update_status(self):
        if self.openJobs:
            self.heating_on = self.openJobs['heating_on']
            self.status = self.heating_on
            self.openJobs = {}

class Sprinkler(Actuator):
    def __init__(self, uniq_id,position=None):
        super().__init__(uniq_id)
        self.actuator_type = "sprinkler"
        self.water_running = 0  # sprinkler switched on
        self.status = self.water_running
        self.openJobs = {}
        self.position = position

    def update_status(self):
        if self.openJobs:
            self.water_running = self.openJobs['water_running']
            self.status = self.water_running
            self.openJobs = {}

if __name__ == '__main__':
    dummy_dev = SmartLamp(uniq_id='100000')
    dummy_dev.update_status()
