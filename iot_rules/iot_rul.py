import operator

class IOT_Rules:
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list,
                 actuator_value_True, actuator_value_False=None):
        self.uniq_id = uniq_id
        self.sensor_ids = sensor_id_list
        self.actuator_ids = actuator_id_list
        self.data = []
        self.sensor_reading = []
        self.actuator_output = []
        self.actuator_value_True = actuator_value_True
        self.actuator_value_False = actuator_value_False
        self.comparisons = []
        self.thresholds = []
        self.requirement = 'all'

    def rule_decision(self):
        comp_operators = [{'>': operator.gt, '<': operator.lt, '=': operator.eq, '!=': operator.ne, }[comp] for
                          comp in self.comparisons]
        values = [comp_op(val, thresh) for comp_op, val, thresh in zip(comp_operators, self.data, self.thresholds)]
        if self.requirement == 'all':
            return all(values)
        return any(values)


class SmartStreetLight(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list,
                 actuator_value_True, actuator_value_False=None):
        super().__init__(uniq_id, sensor_id_list, actuator_id_list,
                 actuator_value_True, actuator_value_False)
        self.sensor_reading = ['motion', 'noise_detector']
        self.actuator_output = ['switch']

        self.comparisons = ['=', '=']
        self.thresholds = [True, True]
        self.requirement = 'all'


class SmartCatDoor(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list,
                 actuator_value_True, actuator_value_False=None, distance_threshold=0.5):
        super().__init__(uniq_id, sensor_id_list, actuator_id_list,
                         actuator_value_True, actuator_value_False)
        self.sensor_reading = ['distance']
        self.actuator_output = ['switch']

        self.comparisons = ['<']
        self.thresholds = [distance_threshold]
        self.requirement = 'all'


class SmartFloodLight(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id, sensor_id_list, actuator_id_list)
        self.sensor_reading = ['motion', 'noise_detector']
        self.actuator_output = ['switch' for _ in actuator_id_list]

        self.comparisons = ['=', '=']
        self.thresholds = [True, True]
        self.requirement = 'all'


if __name__ == '__main__':
    # dummy_rul = IOT_Rules(uniq_id='000000')
    # print(dummy_rul.send_actuator_jobs())

    # Quick rules check test
    flood_light = SmartFloodLight('0001', ['s1', 's2'], ['ac1', 'ac2', 'ac3'])
    flood_light.data = [True, False]
    assert not flood_light.rule_decision()
    flood_light.data = [True, True]
    assert flood_light.rule_decision()
    flood_light.data = [False, False]
    assert not flood_light.rule_decision()

    cat_door = SmartCatDoor('0001', ['s1'], ['ac1'])
    cat_door.data = [1.2]
    assert not cat_door.rule_decision()
    cat_door.data = [0.3]
    assert cat_door.rule_decision()
    cat_door.data = [0.7]
    assert not cat_door.rule_decision()
