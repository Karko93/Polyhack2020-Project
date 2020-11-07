from iot_device.actuator import Actuator

class SmartLamp(Actuator):

    def __init__(self):
        self.intensity = 0 # Intensity of the lamp

    def SetIntensity(self, value):
        self.intensity = value
        #Callback to Server is needed
        #Callback to Environment needed
