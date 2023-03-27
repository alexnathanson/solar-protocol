#!/bin/bash

# Run the first Python program and print its comments
echo "Running clientPostIP"
python3 /home/pi/solar-protocol/backend/core/clientPostIP.py

# Run the second Python program and print its comments
echo "Running getRemoteData"
python3 /home/pi/solar-protocol/backend/core/getRemoteData.py

# Run the third Python program and print its comments
echo "Running solarProtocol.py"
python3 /home/pi/solar-protocol/backend/core/solarProtocol.py

echo "createHTML.py"
python3 /home/pi/solar-protocol/backend/createHTML/create-html.py

echo "viz.py"
python3 /home/pi/solar-protocol/backend/createHTML/viz.py
