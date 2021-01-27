#!/bin/bash

sudo chmod a+w /home/pi/local/local.json
sudo chmod a+w /home/pi/solar-protocol/backend/api/v1/deviceList.json
sudo chmod +x /home/pi/solar-protocol/backend/update_ip2.sh
sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py
sudo chmod a+w /home/pi/solar-protocol/frontend/index.html
sudo chmod +x /home/pi/solar-protocol/utilities/update.sh

echo "Permissions set for local.json, deviceList.json, update_ip2.sh, csv_datalogger.py, and index.html"
