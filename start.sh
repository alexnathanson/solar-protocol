#!/bin/bash

#run with:
#sudo /bin/bash start.sh

echo "Starting Solar Protocol!"

sleep 60

echo "done waiting... activating venv"
source /home/pi/solar-protocol/.venv/bin/activate

echo "starting programs..."

echo "running charge controller data logger -> view error logs at solarprotocol/charge-controller/datalogger.log"
python /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &

echo "running Solar Protocol processes -> view error logs at solarprotocol/backend/runner.log"
python /home/pi/solar-protocol/backend > /home/pi/solar-protocol/backend/runner.log 2>&1 &

echo "start program completed... view logs and admin consoles for status info"