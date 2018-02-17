import json
import time
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

while True:
	r = requests.get(url=server_url + '/beacon')
	beacons = json.loads(r.text)
	for beacon in beacons:
		all_macs.append(beacon['macAddress'])
	print("Registrierte Beacons aktualisiert:")
	print(all_macs)
	for x in range(0, 20):
		returnedList = blescan.parse_events(sock, 10)
		print("Bluetooth Geraete gefunden.")
		for bluetoothDevice in returnedList:
			for mac in all_macs:
				if bluetoothDevice['mac'] and mac.lower() == bluetoothDevice['mac'].lower():
					print("success", mac.lower())
					payload = {'macAddress': bluetoothDevice['mac']}
             				headers = {"Content-Type": "application/json"}
             				r = requests.post(server_url + '/beacon', data=json.dumps(payload), headers=headers)
					print(r.status_code)
					print(r.text)
		time.sleep(1)
	time.sleep(300)
