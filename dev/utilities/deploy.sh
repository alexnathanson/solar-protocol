#!/bin/bash
# this script updates each ip with the latest code
while IFS= read ip; do 
    #rsync -ahz --progress ../ "pi@$ip:/home/pi/solar-protocol/"
    echo "$ip"
    ssh "pi@$ip" "git -C /home/pi/solar-protocol stash"
    ssh "pi@$ip" "git -C /home/pi/solar-protocol pull"
    ssh "pi@$ip" "bash /home/pi/solar-protocol/dev/stop"
    ssh "pi@$ip" "bash /home/pi/solar-protocol/dev/build"
    ssh "pi@$ip" "bash /home/pi/solar-protocol/dev/start"
    ssh "pi@$ip" "bash /home/pi/solar-protocol/dev/generate"
done < hostnames.sh
