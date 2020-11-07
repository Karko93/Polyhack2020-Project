# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:34:14 2020

@author: user
"""
import actuator

class smart_door_lock(Actuator):
    
    __init__ smart_door_lock(self,jsonFile):
        self.serial = jsonFile['serial']
        self.isOpen = jsonFile['value']
        
        
        
    def Unlockdoor(self):
        pass
        ### Callback to Server is needed
        
        