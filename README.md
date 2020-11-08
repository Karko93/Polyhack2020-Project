# Polyhack2020-Project - The Mean Squares
## Used Python libraries
Use following command to install the required libraries:
> pip install pandas\
> pip install numpy\
> pip install -U Flask  
> pip install folium  
> pip install matplotlib
---
## Executing Code
1. Start the server with the script "websocket/server.py"
2. Initialize 1000 Sensors and 1000 Actuators and connect them to the server by executing the python script "launcher/run.py"  
  2a. The files "launcher/initialisation_actuator.json" and "launcher/initialisation_sensor.json" contain all existing devices  
  3a. Rules can be either added live from the webbrowser or by editing the config file "iot_rules/rules_config.json"  
3. Go to the URL in your browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
---
## Overview of the files

### launcher
This folder contains files to initialize and run
#### launcher/run.py
This script launches the simulation. It first reads from an initialisation file containing the desired sensors and actuators. It instantiates each of them, connects them to the server, it simulates an environment for the generation of data and it updates all the devices every second.

### websocket
This folder contains the files related to the server and communication
#### websocket/server.py
This script runs the server application. Once this is running, the simulation can be launched from run.py. Besides the Webserver a thread runs in the background to check whether certain rules have to be applied and actuators need to be triggered.
#### websocket/backend.py
The backend of the webserver which stores transferred data and manages the usage.

### iot_rules
This folder contains files related to the rules and parsing the information
#### iot_rules/iot_rul.py
A file that manages the rules that are defined in "iot_rules/rules_config.json"
#### iot_rules/parser.py
Helper file to parse "iot_rules/rules_config.json" for rules.


### iot_device
This folder contains the implementations of the clients (sensors and actuators) as well as the simulation of the artificial environment
#### iot_device/iot_dev.py
File containing the base classes for sensors and actuators
#### iot_device/actuator.py
This script contains every class around the different actuator types and handling.\
All the different special actuator types (e.g. SmartLamp) are defined here which inherits from the parent class Actuator (IOT_Device).
#### iot_device/sensor.py
This script contains every class around the different sensor types and handling.\
All the different special sensor types (e.g. temperature sensor) are defined here which inheritage from the parent class Sensor (IOT_Device).
#### iot_device/environment.py
It defines how the sensor get new data (stochastic model) and also the influence of the actuators to the sensor data depending on sensor type.
#### iot_device/antenna_actuator_sensor.py
This is an example how to implement a device which is both an actuator and sensor (not supported in the web service yet).

### Documents
This folder contains explanatory files such as a presentation describing the project (TheMeanSquares_ASUSChallenge.pdf) and a demo video (Video_demo.mp4) 
