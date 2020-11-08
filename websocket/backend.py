import pandas as pd
from threading import RLock
from datetime import datetime as dt
from iot_rules.parser import RuleBook

class IOT_Server:
    _devices = None
    _rules = None

    def __init__(self):
        # replace this with something that reads a json file listing the devices
        self._devices = {}  # key:value pairs of the form id:device
        self._rules = RuleBook().all_rules
        self.lock = RLock()

    @property
    def devices(self):
        with self.lock:
            return self._devices

    @property
    def rules(self):
        with self.lock:
            return self._rules

    def process_sensor(self, message):
        '''
        :param message: dictionary received from a client device
        :return:
        '''
        # Check ID of device that wrote in. Create the device is it's unkown
        if message['id'] in self.devices:
            dev = self.devices[message['id']]
        else:
            dev = globals()[message['ancestors'][0]](message['id'])
            dev.kind = message['ancestors'][-2]
            self.devices[message['id']] = dev

        dev.add_data(message['data'])

    def process_actuator(self, message):
        '''
        :param message: dictionary received from a client device
        :return:
        '''
        # Check ID of device that wrote in. Create the device is it's unkown
        if message['id'] in self.devices:
            dev = self.devices[message['id']]
        else:
            dev = globals()[message['ancestors'][0]](message['id'])
            dev.kind = message['ancestors'][-2]
            self.devices[message['id']] = dev

        dev.jobs = message['jobs']
        return '1'

    def describe_all_sensors(self):
        with self.lock:
            ids = []
            types = []
            latest_timestamps = []

            for dev in self.devices:
                if self.devices[dev].kind=='Sensor':
                    ids.append(dev)
                    types.append(type(self.devices[dev]).__name__)
                    latest_timestamps.append(dt.utcfromtimestamp(self.devices[dev].data['timestamp'].iloc[-1]))
            device_table = {'ID': ids, 'Type': types, 'Timestamps' : latest_timestamps}
            return device_table

    def describe_all_actuators(self):
        with self.lock:
            ids = []
            types = []
            jobs = []
            for dev in self.devices:
                if self.devices[dev].kind=='Actuator':
                    ids.append(dev)
                    types.append(type(self.devices[dev]).__name__)
                    jobs.append(self.devices[dev].jobs)

            device_table = {'ID': ids, 'Type': types, 'jobs': jobs}
            return device_table


    def get_sensor(self, unq_id):
        if unq_id in self.devices:
            dev = self.devices[unq_id]
            if dev.data is not None:
                return dev.data.to_html()
        else:
            return 'device NOT found'

    # def get_actuator(self, unq_id):
    #     if unq_id in self.devices:
    #         dev = self.devices[unq_id]
    #         if dev.data is not None:
    #             return dev.data.to_html()
    #     else:
    #         return 'device NOT found'


class IOT_Device():
    uniq_id = None
    data = None
    kind = None

    def __init__(self, uniq_id):
        self.uniq_id = uniq_id

    def add_data(self, data):
        if self.data is None:
            self.data = pd.DataFrame(data, index=[0])
        else:
            self.data = self.data.append(data, ignore_index=True)
        # print(self.data)


class Sensor(IOT_Device):
    pass


class PhysicalSensor(Sensor):
    pass


class TemperatureSensor(Sensor):
    pass


class HumiditySensor(Sensor):
    pass


class MotionSensor(Sensor):
    pass


class NoiseSensor(Sensor):
    pass


class BrightnessSensor(Sensor):
    pass

class ProximitySensor(Sensor):
    pass


class Actuator(IOT_Device):
    jobs = None

    def __init__(self, id):
        super().__init__(id)
        self.jobs = {}

class SmartLamp(Actuator):
    pass

if __name__ == '__main__':
    environmental_sensor = Sensor('temp_sensor_1', ['temperature', 'humidity'])
    door_positioner = Actuator('door_positioner_1', ['door_position'])

    iot_server = IOT_Server()
    iot_server.devices = {environmental_sensor.uniq_id: environmental_sensor,
                          door_positioner.uniq_id: door_positioner}

