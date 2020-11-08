from iot_device.iot_dev import IOT_Device
from datetime import datetime
import json


class ActuatorInstantiator():

    def __init__(self, sensors=[], new_actuator=[]):
        """
        :param actuators: list of existing actuators
        :param new_actuators: list of new actuator to be added
        """
        Thread.__init__(self)
        self.daemon = True
        self.env = env
        self.actuator = sensors
        self.new_actuator = new_actuator

    def update(self):
        for element in self.new_actuators:
            if element['type'] == 'actuator':
                uniq_id = element['serial']
                position = element['position']
                position_x, position_y = position[0], position[1]
                if element['ancestor'] == 'doorlock':
                    self.actuators.append(SmartDoorLock(uniq_id, position=position))
                elif element['ancestor'] == 'motorposition':
                    self.actuators.append(MotorPosition(uniq_id, position_x=position_x,
                                                        position_y=position_y))
                elif element['ancestor'] == 'sprinkler':
                    self.actuators.append(Sprinkler(uniq_id, position=position))
                elif element['ancestor'] == 'heating':
                    self.actuators.append(Heating(uniq_id, position=position))
                elif element['ancestor'] == 'smartlamp':
                    self.actuators.append(SmartLamp(uniq_id, position=position))
                else:
                    pass
            self.new_sensors.remove(element)
        return self

    def add_actuator(self, actuator):
        """
        :param actuator: dictionary of the same format of the initialisation file.
        :return: self
        """

        self.new_actuators.append(actuator)
        return self

    def run(self):
        while True:
            self.update()
            sleep(0.1)

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
