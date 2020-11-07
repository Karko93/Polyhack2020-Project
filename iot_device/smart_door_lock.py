from iot_device.actuator import Actuator

class SmartDoorLock(Actuator):
    
    def __init__(self, jsonFile):
        self.isDoorLocked = True # State if door is locked
        self.LockDoor()

        
        
    def UnlockDoor(self):
        self.doorLocked = False
        ### Callback to Server is needed
        ### Callback to Environment needed
        
    
    def LockDoor(self):
        self.doorLocked = True
        ### Callback to Server is needed
        ### Callback to Environment needed
        
    
