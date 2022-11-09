#!/usr/bin/env bash

# This script is used to force the DNS to update directly.
# It is used for testing if the DNS is working and connects to the server.
# It does not go through the DNS gateway.
# The first argument should be the DNS password.

set -e # exit on first error
set -u # error out if any variables are unset

# Variables
LOGFILE=/var/log/namecheap.log
HOST=@
DOMAIN=solarprotocol.net
PASSWORD=$1

# Get current time
TIME=$(date +%Y-%m-%d:%H:%M)
echo "TIME: $TIME"

# Get current IP
IP=$(curl --insecure --silent https://dynamicdns.park-your-domain.com/getip)
echo "IP: $IP"

# Update Namecheap DDNS
RESPONSE=$(curl --insecure --silent "https://dynamicdns.park-your-domain.com/update?host=${HOST}&domain=${DOMAIN}&password=${PASSWORD}&ip=${IP}")
echo "RESPONSE: "
echo $RESPONSE

# Log the time and IP
echo "$TIME - $IP" >> $LOGFILE