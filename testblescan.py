import json

import bluetooth._bluetooth as bluez
import requests

import blescan

all_macs = []

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")

except:
    print("error accessing bluetooth device...")

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

server_url = 'http://10.200.20.150:8080'
r = requests.get(url=server_url + '/beacon')

beacons = json.loads(r.text)

for beacon in beacons:
	all_macs.append(beacon['macAddress'])

print(all_macs)

# while True:
#     returnedList = blescan.parse_events(sock, 10)
#     print("----------")
#     for beacon in returnedList:
#         print(beacon)
#         if beacon['mac'] == 'cb:d0:ac:84:ed:2f':
#             payload = {'senderID': 'pi1', 'beaconID': 'beacon_a', 'distanceToBeacon': 4.2, 'timestamp': '12:34'}
#             headers = {"Content-Type": "application/json"}
#             r = requests.post(url + '/push', data=json.dumps(payload), headers=headers)
#             print(r.status_code)
#             print(r.text)
#             break
