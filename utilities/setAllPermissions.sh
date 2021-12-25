#!/bin/bash

sudo chmod a+w /home/pi/local/.spenv
sudo chmod a+w /home/pi/local/local.json
sudo chmod a+w /home/pi/local/access.json
sudo chmod -R a+w /home/pi/local/www
sudo chmod a+w /home/pi/solar-protocol/backend/data/deviceList.json
sudo chmod a+w /home/pi/solar-protocol/backend/data/poe.log
sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py
sudo chmod a+w /home/pi/solar-protocol/frontend/index.html
sudo chmod +x /home/pi/solar-protocol/utilities/update.sh
sudo chmod a+w /home/pi/solar-protocol/frontend/images/clock-exhibit.png
echo "Permissions set for local www directory, local.json, deviceList.json, csv_datalogger.py, and index.html"
