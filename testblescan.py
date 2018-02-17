# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import requests
import json
import bluetooth._bluetooth as bluez


allBeacons = []

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	print "----------"
	for beacon in returnedList:
		print beacon
                if beacon['mac'] == 'cb:d0:ac:84:ed:2f':
			url = 'http://10.200.18.137:8080/beacon'
			payload = {'senderID': 'pi1', 'beaconID': 'beacon_a', 'distanceToBeacon': 4.2, 'timestamp': '12:34'}
			headers = {"Content-Type": "application/json"}
			r = requests.post(url + '/push', data=json.dumps(payload), headers=headers)
			print(r.status_code)
			print(r.text)
			break
