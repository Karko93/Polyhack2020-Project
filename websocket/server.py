from flask import Flask, request, render_template
import requests
import json
from websocket.backend import IOT_Server
from websocket.helper import html_table
app = Flask(__name__, template_folder='html')

iot_server = IOT_Server()

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/devices')
def devices():
    return html_table(iot_server.describe_all_devices())

@app.route('/devices/<unq_id>')
def show_device(unq_id):
    return iot_server.get_device(unq_id)

@app.route('/sensor_com', methods=['POST'])
def sensor_com():
    jsondata = request.get_json()
    message = json.loads(jsondata)
    print(message)
    iot_server.process_sensor(message)
    return '0'

@app.route('/actuator_com', methods=['POST'])
def actuator_com():
    jsondata = request.get_json()
    message = json.loads(jsondata)
    print(message)
    return json.dumps(iot_server.process_sensor(message))

@app.route('/send_json', methods=['GET'])
def send_json():
    result = {'escalate': True}
    # stuff happens here that involves data to obtain a result
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)
