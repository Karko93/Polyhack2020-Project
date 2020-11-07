
class IOT_Server:
    devices = None
    rules = None

    def __init__(self):
        # replace this with something that reads a json file listing the devices
        self.devices = {}  # key:value pairs of the form id:device
        self.rules = []

    def process_message(self, message):
        '''
        :param message: dictionary received from a client device
        :return:
        '''
        # Check ID of device that wrote in. Create the device is it's unkown
        if message['id'] in self.devices:
            dev = self.devices[message['id']]
        else:
            if 'data' not in message:
                return {}
            data_names = list(message['data'].keys())
            if 'Actuator' in message['ancestors']:
                dev = Actuator(message['id'], data_names)
            else:
                dev = Sensor(message['id'], data_names)
            self.devices[message['id']] = dev


        # store device data (sensor data, actuator state, ...)
        if 'data' in message:
            dev.add_data(message['data'])

        response = {}  # Store default respons value here (e.g. {'success':True})

        # If the device is an actuator, tell it what it should do
        if type(dev) is Actuator:
            for job_name, job_value in dev.jobs():
                response['job_name'] = job_value

        return response

    # check whether this triggers any rules (in a thread)

    def describe_all_devices(self):
        devices_string = '\n\n'.join([dev.describe_device() for dev in self.devices.values()])
        return devices_string if devices_string else 'None'


class IOT_Device():
    id = None
    data = None

    def __init__(self, id, data_names):
        self.id = id
        self.data = {data_name: [] for data_name in data_names}

    def add_data(self, data):
        for key, value in data.items():
            self.data[key].append(value)

    def describe_device(self):
        data_string = '        \n'.join(['{}:{}'.format(key, value) for key, value in self.data.items()])
        out = ('Device name: {name}\n'
               '  data: {data}').format(name=self.id,
                                        data=data_string)
        return out


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

