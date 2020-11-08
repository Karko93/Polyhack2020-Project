## Client-Server communication

Messages sent back and forth between the server and client are dictionaries.

### Client side communication

All clients communication must contain the following fields:
- `'id'`: a unique identifier for the device
- `'ancestors'`: a list of inheritance of the device in question, in order from
youngest to oldest (e.g. `['TemperatureSensor', 'Sensor', 'IOT_Device']`)
- `'data'`: a dictionary of data to store on the server

Clients are either `Sensor` or `Actuator`. The main difference between the two, is
that a `Sensor` object will not get any response from the server, while an `Actuator`
 object will


### Server side communication

The server will receive messages from the client, and store the received data locally.
If an actuator needs actuating, the server will wait until the next time the actuator
contacts the server, and will return the job to do be executed by the actuator.

In principle, a `Sensor` sends data to the server and that's it. An `Actuator` however,
expects a response from the server telling it whether or not it needs to do anything.

The response from the server will be a list of jobs to do, that it gets from the rules engine.
If there's nothing to be done, the response will be an empty dictionary. 
If there is something to do, the dictionary will list what values to change. E.g. if
a door should be unlocked, the response will be:  `{'DoorLocked': False}`.



