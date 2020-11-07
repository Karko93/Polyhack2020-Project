from flask import Flask, request
import requests
import json
from websocket.backend import IOT_Server

app = Flask(__name__)

iot_server = IOT_Server()

@app.route('/')
def default():
    return iot_server.describe_all_devices()

@app.route('/recv_json', methods=['POST'])
def recv_json():
    jsondata = request.get_json()
    message = json.loads(jsondata)
    print(message)
    return json.dumps(iot_server.process_message(message))

@app.route('/send_json', methods=['GET'])
def send_json():
    result = {'escalate': True}
    # stuff happens here that involves data to obtain a result
    return json.dumps(result)

if __name__ == '__main__':

    app.run(debug=True)
