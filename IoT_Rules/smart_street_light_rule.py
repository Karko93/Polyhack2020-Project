from iot_rul import IOT_Rules


class SmartStreetLight(IOT_Rules):

    def __init__(self,uniq_id):
        super().__init__(uniq_id)

    def rule_decision(self):
        # Switches the light on if both of the sensors (motion and noise) detect something
        if (self.data[0] == True and self.data[1] == True):
            return True
        else:
            return False
