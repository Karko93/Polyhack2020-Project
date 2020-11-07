import json
import requests

class IOT_Device:
    hostname = 'http://127.0.0.1:5000/'
    initialized = False
    ancestors = []
    def __init__(self, id):
        self.id = id
        self.get_hierarchy()

    def _post(self, address, message):
        """Wrapper function for POST interaction with the server."""
        s = json.dumps(message)
        host = self.hostname + address
        try:
            return int(requests.post(host, json=s).content)
        except:
            return 1

    # def init_at_host(self):
    #     """Call the host for the first time and pass its object information."""
    #     message = {'id': self.id, 'ancestors': self.ancestors}
    #     retval = self._post('recv_json', message)
    #     if retval == 0:
    #         self.initialized = True

    def get_hierarchy(self):
        """Get all parent classes and its own class of an instance and store them as a member variable ancestors"""
        cls = type(self)
        while cls.__name__ != 'object':
            self.ancestors.append(cls.__name__)
            cls = cls.__bases__[0]

if __name__ == '__main__':
    dummy_dev = IOT_Device(id='000000')
    print(dummy_dev.get_hierarchy())
