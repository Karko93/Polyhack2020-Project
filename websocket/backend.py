import pandas as pd

class IOT_Server:
    devices = None
    rules = None

    def __init__(self):
        # replace this with something that reads a json file listing the devices
        self.devices = {}  # key:value pairs of the form id:device
        self.rules = []

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
            self.devices[message['id']] = dev

        dev.add_data(message['data'])


    def describe_all_devices(self):
        ids = [dev for dev in self.devices]
        types = [type(self.devices[dev]).__name__ for dev in self.devices]
        device_table = {'ID': ids, 'Type': types}
        return device_table

    def get_device(self, unq_id):
        if unq_id in self.devices:
            dev = self.devices[unq_id]
            if dev.data is not None:
                return dev.data.to_html()
        else:
            return 'device NOT found'

class IOT_Device():
    id = None
    data = None

    def __init__(self, id):
        self.id = id

    def add_data(self, data):
        if self.data is None:
            self.data = pd.DataFrame(data, index=[0])
        else:
            self.data = self.data.append(data, ignore_index=True)
        print(self.data)


class Sensor(IOT_Device):
    pass


class Actuator(IOT_Device):
    jobs = None

    def __init__(self, id, data_names):
        super().__init__(id, data_names)
        self.jobs = {}

    def describe_device(self):
        data_string = '        \n'.join(['{}:{}'.format(key, value) for key, value in self.data.items()])
        jobs_string = '        \n'.join(['{}:{}'.format(key, value) for key, value in self.jobs.items()])
        out = ('Device name: {name}\n'
               '  data: {data}\n'
               '  jobs: {jobs}').format(name=self.id,
                                        data=data_string,
                                        jobs=jobs_string)
        return out


if __name__ == '__main__':
    environmental_sensor = Sensor('temp_sensor_1', ['temperature', 'humidity'])
    door_positioner = Actuator('door_positioner_1', ['door_position'])

    iot_server = IOT_Server()
    iot_server.devices = {environmental_sensor.id: environmental_sensor,
                          door_positioner.id: door_positioner}

