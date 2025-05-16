import json
import urequests

URL = const("http://10.0.0.14:5000/data")


def send(host, rssi, timestamp, package_delay_ms, msg):
    data = dict(
        mac=host.hex(),
        rssi=rssi,
        timestamp=timestamp,
        package_delay_ms=package_delay_ms,
        locality="Siemensstr. 4",
        data=msg.hex(),
    )
    response = urequests.post(URL, json=json.dumps(data))

    if response.status_code == 200:
        print("Success!")
        print("Response:", response.json())
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:", response.text)


def test_requests():
    json = '{"mac_address": "AA:BB:CC:DD:EE:FF","rssi": -10,"data": "test curl"}'
