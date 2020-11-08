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
        dev.data = dev.data.iloc[-50:]

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
        dev.add_data(message['data'])
        dev.data = dev.data.iloc[-50:]
        return dev.jobs

    def describe_all_sensors(self):
        with self.lock:
            ids = []
            types = []
            latest_timestamps = []

            for dev in self.devices:
                if self.devices[dev].kind=='Sensor':
                    ids.append(dev)
                    types.append(type(self.devices[dev]).__name__)
                    ts = self.devices[dev].data['timestamp'].iloc[-1]
                    if isinstance(ts, int):
                        latest_timestamps.append(dt.utcfromtimestamp(self.devices[dev].data['timestamp'].iloc[-1]))
                    else:
                        latest_timestamps.append(ts)

            device_table = {'ID': ids, 'Type': types, 'Timestamps' : latest_timestamps}
            return pd.DataFrame(device_table).sort_values('ID').to_html()

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
            return pd.DataFrame(device_table).sort_values('ID').to_html()

    def describe_all_rules(self):
        with self.lock:
            # print(dir(self.rules[0]))
            # ids = []
            # types = []
            all_params = []
            for rule in self.rules:
                members = dir(rule)
                members = [mem for mem in members if not mem.startswith('__')]
                members.remove('uniq_id')
                members.remove('rule_decision')
                members.remove('data')
                members = ['uniq_id'] + members
                params = {mem: getattr(rule, mem) for mem in members}
                all_params.append(params)
            return pd.DataFrame(all_params)[members].to_html()

            #         ids.append(rule)
            #         types.append(type(self.devices[dev]).__name__)
            #         jobs.append(self.devices[dev].jobs)

            # device_table = {'ID': ids, 'Type': types, 'jobs': jobs}
            # return device_table


    def get_sensor(self, unq_id):
        if unq_id in self.devices:
            dev = self.devices[unq_id]
            if dev.data is not None:
                return dev.data.to_html()
        else:
            return 'device NOT found'

    def get_actuator(self, unq_id):
        if unq_id in self.devices:
            dev = self.devices[unq_id]
            if dev.data is not None:
                return dev.data.to_html()
        else:
            return 'device NOT found'


class IOT_Device():
    def __init__(self, uniq_id):
        self.uniq_id = uniq_id
        self.data = None
        self.kind = None

    def add_data(self, data):
        print(data)
        if not isinstance(data['timestamp'], str):
            data['timestamp'] = dt.utcfromtimestamp(data['timestamp'])
        # data['timestamp'] = data['timestamp']
        if self.data is None:
            self.data = pd.DataFrame(data, index=[0])
        else:
            self.data = self.data.append(data, ignore_index=True)


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


class DistanceSensor(Sensor):
    pass


class AirQualitySensor(Sensor):
    pass


class Actuator(IOT_Device):
    jobs = None

    def __init__(self, id):
        super().__init__(id)
        self.jobs = {}

class SmartLamp(Actuator):
    pass

class SmartDoorLock(Actuator):
    pass

class MotorPosition(Actuator):
    pass

class Heating(Actuator):
    pass

class Sprinkler(Actuator):
    pass



if __name__ == '__main__':
    environmental_sensor = Sensor('temp_sensor_1', ['temperature', 'humidity'])
    door_positioner = Actuator('door_positioner_1', ['door_position'])

    iot_server = IOT_Server()
    iot_server.devices = {environmental_sensor.uniq_id: environmental_sensor,
                          door_positioner.uniq_id: door_positioner}

