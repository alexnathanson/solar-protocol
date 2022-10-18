#!/bin/bash
#
# This script grabs devices.json from the active server

set -e

# make sure script works when called from any directory
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null

scp solarprotocol.net:~/solar-protocol/backend/data/deviceList.json /dev/stdout \
  | jq >| ../data/devices.json

git status --short
