import operator

class IOT_Rules:
    def __init__(self, uniq_id, sensor_id_list, sensor_reading, actuator_id_list,
                 actuator_output, comparisons, thresholds,
                 actuator_value_True, actuator_value_False=None, requirement='all'):
        self.uniq_id = uniq_id
        self.sensor_ids = sensor_id_list
        self.actuator_ids = actuator_id_list
        self.sensor_reading = sensor_reading
        self.actuator_output = actuator_output
        self.actuator_value_True = actuator_value_True
        self.actuator_value_False = actuator_value_False
        self.comparisons = comparisons
        self.thresholds = thresholds
        self.requirement = requirement

        self.data = []

    def rule_decision(self):
        comp_operators = [{'>': operator.gt, '<': operator.lt, '=': operator.eq, '!=': operator.ne, }[comp] for
                          comp in self.comparisons]
        values = [comp_op(val, thresh) for comp_op, val, thresh in zip(comp_operators, self.data, self.thresholds)]
        if self.requirement == 'all':
            return all(values)
        return any(values)


class SmartStreetLight(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list,
                 actuator_value_True=[1], actuator_value_False=None):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=actuator_value_True,
                         actuator_value_False=actuator_value_False,
                         sensor_reading=['motion', 'noise_detector'],
                         actuator_output=['intensity'],
                         comparisons=['=', '='],
                         thresholds=[True, True],
                         requirement='all'
                         )




class SmartCatDoor(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list, distance_threshold=0.5):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[0],
                         actuator_value_False=[1],
                         sensor_reading=['distance'],
                         actuator_output=['door_locked'],
                         comparisons=['<'],
                         thresholds=[distance_threshold],
                         requirement='all')


class SmartFloodLight(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1 for _ in actuator_id_list],
                         sensor_reading=['motion', 'noise_detector'],
                         actuator_output=['intensity' for _ in actuator_id_list],
                         comparisons=['=', '='],
                         thresholds=[True, True],
                         requirement='all'
                         )

class FireEmergency(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1],
                         sensor_reading=['temperature', 'noise_detector'],
                         actuator_output=['sprinkler'],
                         comparisons=['>', '='],
                         thresholds=[30, True],
                         requirement='all'
                         )

class PlantWatering(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1 for _ in actuator_id_list],
                         sensor_reading=['humidity', 'brightness'],
                         actuator_output=['sprinkler'  for _ in actuator_id_list],
                         comparisons=['<', '<'],
                         thresholds=[50, 50],
                         requirement='all'
                         )

class EmergencyDoor(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list, distance_threshold=5.0):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1],
                         actuator_value_False=[0],
                         sensor_reading=['noise_detector', 'distance', 'brightness'],
                         actuator_output=['door_locked'],
                         comparisons=['>', '>', '<'],
                         thresholds=[True, distance_threshold, 50],
                         requirement='all'
                         )

class SmartHeater(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list, temperature_threshold=21.0):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1],
                         actuator_value_False=[0],
                         sensor_reading=['temperature', 'motion'],
                         actuator_output=['heating'],
                         comparisons=['<', '='],
                         thresholds=[temperature_threshold,  True],
                         requirement='all'
                         )

class AdjustLight(IOT_Rules):
    def __init__(self, uniq_id, sensor_id_list, actuator_id_list):
        super().__init__(uniq_id=uniq_id,
                         sensor_id_list=sensor_id_list,
                         actuator_id_list=actuator_id_list,
                         actuator_value_True=[1 for _ in actuator_id_list],
                         sensor_reading=['brightness'],
                         actuator_output=['intensity' for _ in actuator_id_list],
                         comparisons=['='],
                         thresholds=[True],
                         requirement='all'
                         )

    def rule_decision(self):
        self.actuator_value_True = [(100 - self.data[0])/100 for _ in self.actuator_output]
        return True


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
