from iot_device.iot_dev import IOT_Device

class Actuator(IOT_Device):
    jobs = {'light_on': {}}
    def __init__(self, id):
        super().__init__(id)

    def trigger_light(self, on_off):
        pass
