from flask import Flask, request, render_template
import requests
import json
from websocket.backend import IOT_Server
from websocket.helper import BackgroundWorker
from iot_rules.iot_rul import IOT_Rules
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
    return iot_server.describe_all_sensors()

@app.route('/actuators')
def actuators():
    return iot_server.describe_all_actuators()

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
    devices = iot_server.devices
    sensors_list = {k:'{} ({})'.format(type(v).__name__ , k)
                    for k, v in devices.items() if v.kind=='Sensor'}
    # sensors_list = {'000001':'Temperature', '000002':'Humidity'}
    conditions_list = ['>', '<', '=', '!=']
    actuators_list = {k:'{} ({})'.format(type(v).__name__ , k)
                    for k, v in devices.items() if v.kind=='Actuator'}

    # stuff happens here that involves data to obtain a result
    if request.method == 'POST':
        if 'Submit Rule' in request.form:
            # Submit Rule
            ids = [int(rule.uniq_id) for rule in iot_server.rules]
            new_id = 0
            while new_id in ids:
                new_id += 1
            uniq_id = str(new_id).zfill(6)
            rule = IOT_Rules(uniq_id,
                             sensor_id_list=[request.form['sensor_id']],
                             sensor_reading=[request.form['sensor_reading']],
                             actuator_id_list=[request.form['actuator_id']],
                             actuator_output=[request.form['actuator_action']],
                             comparisons=[request.form['condition']],
                             thresholds=[request.form['threshold']],
                             actuator_value_True=[request.form['true_value']],
                             actuator_value_False=[request.form['false_value']] if request.form['false_value'] else None,
                             requirement='all')
            iot_server.rules.append(rule)

            return render_template('rules_generator.html',
                                   sensors_list=sensors_list,
                                   conditions_list=conditions_list,
                                   actuators_list=actuators_list,
                                   )
        required_inputs = ['sensor_id', 'sensor_reading', 'condition', 'threshold', 'actuator_id', 'actuator_action',
                           'true_value', 'false_value']
        request_ready = all(key in request.form for key in required_inputs) and request.form['threshold'] and request.form['true_value']
        sensor_readings = devices[request.form['sensor_id']].data.columns if 'sensor_id' in request.form else []
        actuator_actions = devices[request.form['actuator_id']].data.columns if 'actuator_id' in request.form else []

        return render_template('rules_generator.html',
                               sensors_list=sensors_list,
                               selected_sensor=request.form['sensor_id'] if 'sensor_id' in request.form else None,
                               sensor_readings=sensor_readings,
                               selected_reading=request.form['sensor_reading'] if 'sensor_reading' in request.form else None,
                               conditions_list=conditions_list,
                               selected_condition=request.form['condition'] if 'condition' in request.form else None,
                               threshold=request.form['threshold'] if 'threshold' in request.form else None,
                               actuators_list=actuators_list,
                               selected_actuator=request.form['actuator_id'] if 'actuator_id' in request.form else None,
                               actuator_actions=actuator_actions,
                               selected_action=request.form['actuator_action'] if 'actuator_action' in request.form else None,
                               request_ready=request_ready,
                               true_value=request.form['true_value'] if 'true_value' in request.form else None,
                               false_value=request.form['false_value'] if 'false_value' in request.form else None,
                              )
    return render_template('rules_generator.html',
                           sensors_list=sensors_list,
                           conditions_list=conditions_list,
                           actuators_list=actuators_list,
                          )

if __name__ == '__main__':
    app.run()
