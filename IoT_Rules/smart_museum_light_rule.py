from IoT_Rules.iot_rul import IOT_Rules

class SmartMuseumsLight(IOT_Rules):
    
 
    def rule_decision(self):
        if self.data[0] == True:
            return [True for i in range(len(self.actuator_ids))]
        else:
            return [False for i in range(len(self.actuator_ids))]
        
