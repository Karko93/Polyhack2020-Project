# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:34:14 2020

@author: user
"""
from actuator import Actuator

class SmartDoorLock(Actuator):
    
    def __init__(self, jsonFile):
        self.serial = jsonFile['serial'] # given serial number
        self.doorLocked = True # State if door is locked
        self.LockDoor()

        
        
    def UnlockDoor(self):
        self.doorLocked = False
        ### Callback to Server is needed
        
    
    def LockDoor(self):
        self.doorLocked = True
        ### Callback to Server is needed
        
    
    