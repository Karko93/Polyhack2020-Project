from iot_rul import IOT_Rules
import operator

class GenericRule(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, sensor_quantity, actuator_id_list, actuator_ouput, thresholds, comparisons, requirement='all'):
        super().__init__(uniq_id, sensor_id_list, actuator_id_list)

        self.comp_operators = [{'>':operator.gt, '<':operator.lt, '=':operator.eq, '!=':operator.ne,}[comp] for comp in comparisons]
        self.thresholds = thresholds
        self.requirement = requirement

    def rule_decision(self):
        values = [comp_op(val, thresh) for comp_op, val, thresh in zip(self.comp_operators, self.data, self.thresholds)]
        if self.requirement == 'all':
            return all(values)
        return any(values)

class SmartStreetLight(GenericRule):
    # Switches the light on if both of the sensors (motion and noise) detect something
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         thresholds[True, True],
                         comparisons['=', '='],
                         requirement='all')

if __name__=="__main__":
    ssl = SmartStreetLight('011110', ['0', '0'], ['2'])
    print(ssl.rule_decision())
    ssl.data = [1,0]
    print(ssl.rule_decision())
    ssl.data = [1,1]
    print(ssl.rule_decision())