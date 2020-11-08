from environment import Environment
from sensor import *
from threading import Thread
from time import sleep


class EnvironmentManager(Thread):

    def __init__(self, env):
        Thread.__init__(self)
        self.env = env
        self.daemon = True

    def run(self):
        while True:
            self.env.update_environment()
            sleep(0.1)

# class IOTDeviceThread(Thread):
#     def __init__(self, device):
#         self.device = device
#         self.name = self.device.

if __name__=='__main__':
    env = Environment()
    sensors = []

    counter = 0

    for id in range(5):
        sensors.append(TemperatureSensor(str(counter).zfill(6), env))
        counter += 1

    for id in range(5):
        sensors.append(HumiditySensor(str(counter).zfill(6), env))
        counter += 1

    for id in range(5):
        sensors.append(NoiseSensor(str(counter).zfill(6), env))
        counter += 1

    for id in range(5):
        sensors.append(MotionSensor(str(counter).zfill(6), env))
        counter += 1

    for id in range(10):
        sensors.append(BrightnessSensor(str(counter).zfill(6), env))
        counter += 1

    clock = EnvironmentManager(env)
    clock.start()

    while True:
        for sensor in sensors:
            data = sensor.data
            # print(sensor.uniq_id, data)
            sensor.send_to_server(data)
        sleep(1)
