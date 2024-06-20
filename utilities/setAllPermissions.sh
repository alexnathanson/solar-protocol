#!/bin/bash

sudo chmod a+w /home/sp/local/.spenv
sudo chmod a+w /home/sp/local/local.json
sudo chmod a+w /home/sp/local/access.json
sudo chmod -R a+w /home/sp/local/www
sudo chmod -R a+w /home/sp/local/data
sudo chmod a+w /home/sp/solar-protocol/backend/data/deviceList.json
sudo chmod a+w /home/sp/solar-protocol/backend/data/poe.log
sudo chmod +x /home/sp/solar-protocol/charge-controller/csv_datalogger.py
sudo chmod +x /home/sp/solar-protocol/backend/alt-runner.sh
sudo chmod -R +x /home/sp/solar-protocol/backend
sudo chmod -R +x /home/sp/solar-protocol/backend/createHTML
sudo chmod -R +x /home/sp/solar-protocol/backend/createHTML/viz-assets
sudo chmod -R +x /home/sp/solar-protocol/backend/core

sudo chmod a+w /home/sp/solar-protocol/frontend/index.html
sudo chmod +x /home/sp/solar-protocol/utilities/update.sh
sudo chmod a+w /home/sp/solar-protocol/frontend/images/clock-exhibit.png
echo "Permissions set for local/www directory, backend directory, local/data directory, local.json, deviceList.json, csv_datalogger.py, and index.html"
