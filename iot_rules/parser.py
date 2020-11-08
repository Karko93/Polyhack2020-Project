import json
import iot_rules.iot_rul as rules
import os

class RuleBook:
    all_rules = None
    def __init__(self):
        config_file = os.path.join(os.path.split(__file__)[0], 'rules_config.json')
        with open(config_file) as f:
            data = json.load(f)
            self.all_rules = []
            for d in data:
                params = d.copy()
                params.pop('rule')
                self.all_rules.append(getattr(rules, d['rule'])(**params))


if __name__ == '__main__':
    rb = RuleBook()
