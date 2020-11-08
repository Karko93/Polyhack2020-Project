from iot_device.sensor import PhysicalSensor
from iot_device.actuator import Actuator

class Antenna(PhysicalSensor, Actuator):
    def __init__(self, uniq_id, env, position=None):
        PhysicalSensor.__init__(self,uniq_id, env)
        Actuator.__init__(self,uniq_id)
        
        ## properties of an actuator
        self.actuator_type = "antenna"
        self.isSending = True  # State if door is open
        self.frequency = 1000
        self.openJobs = {}
        self.status = self.isSending
        
        ## properties of a sensor
        self.sensor_type = 'antenna'
        self.position = position
        
        ### actuator method
        def update_status(self):
            if self.openJobs:
                self.isSending = self.openJobs['openSending']
                self.status = self.isSending
                self.openJobs = {}
        
    

    
