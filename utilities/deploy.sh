#!/bin/bash
while IFS= read ip; do 
    #rsync -ahz --progress ../ "pi@$ip:/home/pi/solar-protocol/"
    echo "$ip"
    ssh "pi@$ip" "cd /home/pi/solar-protocol;git stash"
    ssh "pi@$ip" "cd /home/pi/solar-protocol;git pull"
    ssh "pi@$ip" "sh /home/pi/solar-protocol/utilities/setAllPermissions.sh"
    ssh "pi@$ip" "sudo mv /home/pi/solar-protocol/backend/config-files/solarpunk.solarprotocol.net.conf /etc/apache2/sites-available/"
    ssh "pi@$ip" "sudo a2ensite /etc/apache2/sites-available/solarpunk.solarprotocol.net.conf"
    ssh "pi@$ip" "sudo service apache2 restart or sudo systemctl reload apache2"
    ssh "pi@$ip" "python3 /home/pi/solar-protocol/backend/createHTML/create_html.py"
done < hostnames.sh