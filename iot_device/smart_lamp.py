# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:22:22 2020

@author: user
"""
from actuator import Actuator

class SmartLamp(Actuator):

    def __init__(self):
        self.intensity = 0 # Intensity of the lamp

    def SetIntensity(self, value):
        self.intensity = value
        #Callback to Server is needed
        #Callback to Environment needed