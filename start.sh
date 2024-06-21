#!/bin/bash

echo "Starting Solar Protocol!"

sleep 60

echo "done waiting... activating venv"
source /home/pi/solar-protocol/.venv/bin/activate

echo "starting programs..."
python /home/sp/solar-protocol/charge-controller/csv_datalogger.py &
python /home/sp/solar-protocol/backend &