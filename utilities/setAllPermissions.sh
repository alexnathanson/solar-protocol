#!/bin/bash

sudo chmod a+w /home/pi/local/.spenv
sudo chmod a+w /home/pi/local/local.json
sudo chmod a+w /home/pi/local/access.json
sudo chmod -R a+w /home/pi/local/www
sudo chmod -R a+w /home/pi/local/data

sudo chmod a+w /home/pi/solar-protocol/backend/data/deviceList.json
sudo chmod a+w /home/pi/solar-protocol/backend/data/poe.log

sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py
sudo chmod 777 /home/pi/solar-protocol/charge-controller/data

sudo chmod +x /home/pi/solar-protocol/backend/alt-runner.sh
sudo chmod -R +x /home/pi/solar-protocol/backend
sudo chmod -R +x /home/pi/solar-protocol/backend/createHTML
sudo chmod -R +x /home/pi/solar-protocol/backend/createHTML/viz-assets
sudo chmod -R +x /home/pi/solar-protocol/backend/core
sudo chmod 777 /home/pi/solar-protocol/backend/data

sudo chmod a+w /home/pi/solar-protocol/frontend/index.html
sudo chmod +x /home/pi/solar-protocol/utilities/update.sh
sudo chmod a+w /home/pi/solar-protocol/frontend/images/clock-exhibit.png
echo "Permissions set for local/www directory, backend directory, local/data directory, local.json, deviceList.json, csv_datalogger.py, and index.html"
