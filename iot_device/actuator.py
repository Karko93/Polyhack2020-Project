from iot_device.iot_dev import IOT_Device
from datetime import datetime
import json
from time import sleep

class Actuator(IOT_Device):
    def __init__(self, uniq_id):
        super().__init__(uniq_id)
        self.actuator_type = None
        self.status = None
        self.data = None

    def send_to_server(self):
        tsmp = datetime.timestamp(datetime.now())
        self.data['timestamp'] = tsmp
        message = {'id': self.uniq_id, 'ancestors': self.ancestors, 'data': self.data}
        retval = self._post('actuator_com', message)
        return retval

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
                self.data[job] = retval[job]

class SmartLamp(Actuator):
    def __init__(self, uniq_id, position=None):
        super().__init__(uniq_id)
        self.data = {'intensity': 0}
        self.actuator_type = 'light'
        self.position = position

class SmartDoorLock(Actuator):
    def __init__(self, uniq_id, position=None):
        super().__init__(uniq_id)
        self.data = {'door_locked': 0}
        self.actuator_type = 'lock'
        self.position = position

class MotorPosition(Actuator):
    def __init__(self, uniq_id, position=None):
        super().__init__(uniq_id)
        self.data = {'position_x': 0,
                     'position_y': 0,
                     }
        self.actuator_type = 'motorposition'
        self.position = position

class Heating(Actuator):
    def __init__(self, uniq_id, position=None):
        super().__init__(uniq_id)
        self.data = {'heater_on': False}
        self.actuator_type = 'heating'
        self.position = position

class Sprinkler(Actuator):
    def __init__(self, uniq_id, position=None):
        super().__init__(uniq_id)
        self.data = {'sprinkler_on': False}
        self.actuator_type = 'sprinkler'
        self.position = position


if __name__ == '__main__':
    dummy_dev = SmartLamp(uniq_id='100000')
    dummy_dev.update_status()
