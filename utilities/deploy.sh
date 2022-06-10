#!/bin/bash
while IFS= read ip; do 
    #rsync -ahz --progress ../ "pi@$ip:/home/pi/solar-protocol/"
    ssh "pi@$ip" "cd /home/pi/solar-protocol;git pull"
    ssh "pi@$ip" "/home/pi/solar-protocol/utilities/setAllpermissions.sh"
    echo "$ip"
done < hostnames.sh
