from iot_rul import IOT_Rules

class SmartCatDoor(IOT_Rules):
    
    def __init__(self,distance_threshold = 0.5):
        self.threshold = distance_threshold
        self.ruleIsTrue = False
        
        
        
    def rule_decision(self):
        if self.data[0] <= self.threshold:
            return True
        else:
            return False
        
        
        
        
        
    