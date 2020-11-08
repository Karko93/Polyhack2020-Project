import json
import iot_rules.iot_rul as rules
import os

class RuleBook:
    all_rules = None
    def __init__(self):
        config_file = os.path.join(os.path.split(__file__)[0], 'rules_config.json')
        with open(config_file) as f:
            data = json.load(f)
            self.all_rules = [getattr(rules, d['rule'])(d['id'],
                                                        d['sensors'],
                                                        d['actuators'],
                                                        d['actuator_value_True'],
                                                        d['actuator_value_False']) for d in data]


if __name__ == '__main__':
    rb = RuleBook()
