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

    beacon_dist_dict = {}

    for x in range(0, 20):
        returnedList = blescan.parse_events(sock, 10)
        print("Scanne Bluetooth Geraete... (" + str(x) + "/20)")
        for bluetoothDevice in returnedList:
            for mac in all_macs:
                if mac.lower() == bluetoothDevice['mac'].lower():
                    print("MAC erkannt: " + str(mac.lower()))

                    distance = math.pow(10, ((bluetoothDevice['txp'] - bluetoothDevice['rssi']) / (10 * 2.75)))

                    if mac in beacon_dist_dict:
                        beacon_dist_dict[mac]['distance'] += distance
                        beacon_dist_dict[mac]['count_updates'] += 1.0
                    else:
                        beacon_dist_dict[mac] = {'mac': mac, 'txp': bluetoothDevice['txp'],
                                                 'rssi': bluetoothDevice['rssi'], 'count_updates': 1,
                                                 'distance': distance}

    for mac in beacon_dist_dict:
        avg_distance = beacon_dist_dict[mac]['distance'] / beacon_dist_dict[mac]['count_updates']
        print("\navg_distance von " + mac + ": " + str(avg_distance))

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        payload = {"senderID": str(pi_mac), "beaconID": mac, "distanceToBeacon": avg_distance,
                   "timestamp": timestamp}
        headers = {"Content-Type": "application/json"}

        print(server_url)
        r = requests.post(server_url + '/distance', data=json.dumps(payload), headers=headers)
        print(str(r.status_code) + '\n')

    print("Warte 5 Sekunden...\n")
    time.sleep(5)
