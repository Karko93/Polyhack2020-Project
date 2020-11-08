# Polyhack2020-Project - The Mean Squares
## Used Python libraries
Use following command to install the required libraries:
> pip install pandas\
> pip install numpy\
> pip install -U Flask
---
## Executing Code
1. Start the server with the script "server.py"
2. Run the python script "run.py"
1. Got to the URL in your browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
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
This script contains every class around the different actuator types and handling.\
All the different special actuator types (e.g. SmartLamp) are defined here which inheritage from the parent class Actuator (IOT_Device).
### sensor.py
This script contains every class around the different sensor types and handling.\
All the different special sensor types (e.g. temperature sensor) are defined here which inheritage from the parent class Sensor (IOT_Device).
### environment.py
It defines how the sensor get new data (stochastic model) and also the influence of the actuators to the sensor data depending on sensor type.
### antenna_actuator_sensor.py
This is an example how to implement a device which is both, an actuator and sensor (not supported in the web service yet).
### test_sensor.py
