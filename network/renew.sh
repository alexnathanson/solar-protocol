#!/bin/bash

function parse_json()
{
    echo $1 | \
    sed -e 's/[{}]/''/g' | \
    sed -e 's/", "/'\",\"'/g' | \
    sed -e 's/" ,"/'\",\"'/g' | \
    sed -e 's/" , "/'\",\"'/g' | \
    sed -e 's/","/'\"---SEPERATOR---\"'/g' | \
    awk -F=':' -v RS='---SEPERATOR---' "\$1~/\"$2\"/ {print}" | \
    sed -e "s/\"$2\"://" | \
    tr -d "\n\t" | \
    sed -e 's/\\"/"/g' | \
    sed -e 's/\\\\/\\/g' | \
    sed -e 's/^[ \t]*//g' | \
    sed -e 's/^"//'  -e 's/"$//'
}

#get certificate with expiration date
sudo certbot certificate > /home/pi/cert.log

while read p; do
  echo "$p"
done < /home/pi/cert.log

echo "Initiating PoE"
source /home/pi/solar-protocol/.venv/bin/activate

python /home/pi/solar-protocol/utilities/updateDNS_UnitTest.py > /home/pi/solar-protocol/network/renewal.log

sudo certbot renew --apache

