#!/bin/bash

cd /home/pi/solar-protocol
git stash
git pull
sudo chmod +x /home/pi/solar-protocol/utilities/setAllPermissions.sh
sh /home/pi/solar-protocol/utilities/setAllPermissions.sh
