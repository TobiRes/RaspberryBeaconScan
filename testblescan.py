import datetime
import json
import math
import time
from uuid import getnode as get_mac

import bluetooth._bluetooth as bluez
import requests

import blescan

all_macs = []
pi_mac = get_mac()

dev_id = 0

try:
    sock = bluez.hci_open_dev(dev_id)

except:
    print("error accessing bluetooth device...")

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

server_url = 'http://10.200.18.137:8080'

while True:

    r = requests.get(url=server_url + '/beacon')
    beacons = json.loads(r.text)
    for beacon in beacons:
        all_macs.append(beacon['macAddress'])
    print("\n\nRegistrierte Beacons aktualisiert:")
    print(all_macs)
    rssi_sum = 0.0
    count = 0.0

    for x in range(0, 20):
        returnedList = blescan.parse_events(sock, 10)
        print("Scanne Bluetooth Geraete... (" + str(x) + "/20)")
        for bluetoothDevice in returnedList:
            for mac in all_macs:
                if bluetoothDevice['mac'] and mac.lower() == bluetoothDevice['mac'].lower():
                    print("MAC erkannt:", mac.lower())
                    rssi_sum += bluetoothDevice['rssi']
                    txp = bluetoothDevice['txp']
                    count += 1.0

    rssi_avg = rssi_sum / count
    distance = math.pow(10, ((txp - rssi_avg) / (10 * 2.75)))

    print('\nrssi_avg: ' + str(rssi_avg))
    print('txp: ' + str(txp))
    print('calculated distance: ' + str(distance))

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    payload = {"senderID": str(pi_mac), "beaconID": bluetoothDevice['mac'], "distanceToBeacon": distance,
               "timestamp": timestamp}
    headers = {"Content-Type": "application/json"}

    print(server_url)
    r = requests.post(server_url + '/distance', data=json.dumps(payload), headers=headers)
    print(r.status_code + '\n\n')
    time.sleep(5)
