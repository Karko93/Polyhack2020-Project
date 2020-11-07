from iot_rul import IOT_Rules

class SmartFloodLight(IOT_Rules):
    def __init__(self,uniq_id):
        super().__init__(uniq_id)
        
        
    def rule_decision(self):
        
        if self.data[0] == True and self.data[1]==True:
            return [True for i in range(len(self.actuator_ids))]
        else:
            return [False for i in range(len(self.actuator_ids))]
        
    