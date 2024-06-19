#!/bin/bash

#this is only used if running the python script directly from rc.local doesn't work for some reason

echo "alt runner"

sleep 60

source /home/pi/solar-protocol/.venv/bin/activate
python /home/pi/solar-protocol/backend