from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recv_json', methods = ['POST'])
def recv_json():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    #stuff happens here that involves data to obtain a result
    print(data)
    return '0'


@app.route('/send_json', methods = ['GET'])
def send_json():
    result = {'escalate': True}
    #stuff happens here that involves data to obtain a result
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
