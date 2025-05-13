import json
import requests
from proxy import sender, rssi, timestamp, msg, URL

URL = const("http://10.0.0.47:5000/sensor-data")

def send(host, rssi, timestamp, msg):
    data = dict(
        host=host.hex(),
        rssi=rssi,
        ts=timestamp,
        data=msg.hex()
    )
    response = requests.post(URL, json=json.dumps(data))

    # Send the POST request

    # Check if the request was successful
    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:", response.text)
