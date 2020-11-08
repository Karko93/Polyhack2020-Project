from flask import Flask, request, render_template
import requests
import json
from websocket.backend import IOT_Server
from websocket.helper import html_table, BackgroundWorker
import threading

# suppress output to console
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='html')

iot_server = IOT_Server()
background_worker = BackgroundWorker(iot_server)
background_worker.start()

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/sensors')
def sensors():
    return html_table(iot_server.describe_all_sensors())

@app.route('/actuators')
def actuators():
    return html_table(iot_server.describe_all_actuators())

@app.route('/rules')
def rules():
    # iot_server.describe_all_rules()
    return iot_server.describe_all_rules()

@app.route('/sensors/<unq_id>')
def show_device(unq_id):
    return iot_server.get_sensor(unq_id)

@app.route('/actuators/<unq_id>')
def show_actuator(unq_id):
    return iot_server.get_actuator(unq_id)


@app.route('/sensor_com', methods=['POST'])
def sensor_com():
    jsondata = request.get_json()
    message = json.loads(jsondata)
    iot_server.process_sensor(message)
    return '0'

@app.route('/actuator_com', methods=['POST'])
def actuator_com():
    jsondata = request.get_json()
    message = json.loads(jsondata)
    return json.dumps(iot_server.process_actuator(message))

@app.route('/send_json', methods=['GET'])
def send_json():
    result = {'escalate': True}
    # stuff happens here that involves data to obtain a result
    return json.dumps(result)


@app.route('/rules_generator', methods=['GET', 'POST'])
def rules_generator():

    # sensors_list and actuators_list should be read from iot_server
    sensors_list = {'000001':'Temperature', '000002':'Humidity'}
    conditions_list = ['>', '<', '=', '!=']
    actuators_list = {'000001':'Heater', '000002':'DoorLock'}

    # stuff happens here that involves data to obtain a result
    if request.method == 'POST':
        if 'Submit Rule' in request.form:
            # Submit Rule
            return render_template('rules_generator.html',
                                   sensors_list=sensors_list,
                                   conditions_list=conditions_list,
                                   actuators_list=actuators_list,
                                   )
        required_inputs = ['sensor_id', 'sensor_reading', 'condition', 'threshold', 'actuator_id', 'actuator_action']
        request_ready = all(key in request.form for key in required_inputs)
        return render_template('rules_generator.html',
                               sensors_list=sensors_list,
                               selected_sensor=request.form['sensor_id'] if 'sensor_id' in request.form else None,
                               sensor_readings=['Reading A', 'Reading B'] if 'sensor_id' in request.form else [],
                               selected_reading=request.form['sensor_reading'] if 'sensor_reading' in request.form else None,
                               conditions_list=conditions_list,
                               selected_condition=request.form['condition'] if 'condition' in request.form else None,
                               threshold=request.form['threshold'] if 'threshold' in request.form else None,
                               actuators_list=actuators_list,
                               selected_actuator=request.form['actuator_id'] if 'actuator_id' in request.form else None,
                               actuator_actions=['Do something', 'Do something else'] if 'actuator_id' in request.form else [],
                               selected_action=request.form['actuator_action'] if 'actuator_action' in request.form else None,
                               request_ready=request_ready
                              )
    return render_template('rules_generator.html',
                           sensors_list=sensors_list,
                           conditions_list=conditions_list,
                           actuators_list=actuators_list,
                          )

if __name__ == '__main__':
    app.run()
