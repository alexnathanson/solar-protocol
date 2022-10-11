#!/bin/bash
#
# This script grabs deviceList.json from the active server

set -e

# make sure script works when called from any directory
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null

scp solarprotocol.net:~/solar-protocol/backend/data/deviceList.json /dev/stdout \
  | jq >| ../backend/data/deviceList.json

git status -- ../backend/data/deviceList.json
