from IoT_Rules.iot_rul import IOT_Rules

class SmartCatDoor(IOT_Rules):
    
    def __init__(self,uniq_id,distance_threshold = 0.5):
        super().__init__(uniq_id)
        self.threshold = distance_threshold
        
        
    def rule_decision(self):
        if self.data[0] <= self.threshold:
            return True
        else:
            return False
        
        
        
        
        
