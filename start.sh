#!/bin/bash

echo "Starting Solar Protocol!"

#sleep 60

echo "done waiting... activating venv"
source /home/pi/solar-protocol/.venv/bin/activate

echo "starting programs..."
#python /home/pi/solar-protocol/charge-controller/csv_datalogger.py &
python /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &

python /home/pi/solar-protocol/backend > /home/pi/solar-protocol/backend/runner.log 2>&1 &