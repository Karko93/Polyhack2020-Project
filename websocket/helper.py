import pandas as pd
from threading import Thread, Lock
from time import sleep

def html_table(table):
    return pd.DataFrame(data=table).to_html()


class BackgroundWorker(Thread):
    def __init__(self, iot_server):
        Thread.__init__(self)
        self.iot_server = iot_server
        self.daemon = True
        self.name = self.__class__.__name__

    def run(self):
        while True:
            device_table = self.iot_server.describe_all_devices()
            print(device_table)
            sleep(5)
