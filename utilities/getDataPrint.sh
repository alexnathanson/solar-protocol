#!/bin/bash

# Run the first Python program and print its comments
echo "Running clientPostIP"
python3 /home/pi/solar-protocol/backend/core/clientPostIP.py | sed -n '/^\s*#/p'

# Run the second Python program and print its comments
echo "Running getRemoteData"
python3 /home/pi/solar-protocol/backend/core/getRemoteData.py | sed -n '/^\s*#/p'

# Run the third Python program and print its comments
echo "Running solarProtocol.py"
python3 /home/pi/solar-protocol/backend/core/solarProtocol.py | sed -n '/^\s*#/p'


