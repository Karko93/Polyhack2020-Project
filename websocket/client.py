import sys
import json
import requests

res = requests.get("http://127.0.0.1:5000/")
print(res.content)

conv = [{'input': 'hi', 'topic': 'Greeting'}]
s = json.dumps(conv)
res = requests.post("http://127.0.0.1:5000/recv_json", json=s)

res = requests.get("http://127.0.0.1:5000/send_json")
print(res.content)
