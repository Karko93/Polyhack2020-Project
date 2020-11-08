# Polyhack2020-Project - The Mean Squares
## Used Python libraries
Use following command to install the required libraries:
> pip install pandas\
> pip install numpy\
> pip install -U Flask
---
## Executing Code

---
## Overview of the scripts

### app.py

### run.py

### server.py

### client.py

### backend.py

### iot_rul.py

### parser.py

### iot_dev.py

### actuator.py

### sensor.py
This script contains every class around the different sensor types and handling.\
All the different special sensor types (e.g. temperature sensor) are defined here which inheritage from the parent class Sensor (IOT_Device).
### environment.py
It defines how the sensor get new data (stochastic model) and also the influence of the actuators to the sensor data depending on sensor type.
### antenna_actuator_sensor.py

### test_sensor.py
