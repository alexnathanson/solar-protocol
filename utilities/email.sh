#!/bin/bash

#email

#based on https://raspberry-projects.com/pi/software_utilities/email/ssmtp-to-send-emails

#INSTALLATION:
#sudo apt-get install ssmtp
#sudo apt-get install mailutils

echo "Hello from the solar server!" | mail -s "Solar Server Alert" recipientname@domain.com