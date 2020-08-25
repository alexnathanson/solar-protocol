# Installation
## OS
Configure device https://www.raspberrypi.org/documentation/configuration/raspi-config.md <br>
* change password, connect to wifi, enable SSH, keyboard layout, set timezone, and any other necessry configurations.
`sudo apt update`<br>
`sudo apt full-upgrade`

## Utilities
`sudo apt-get install git`

## Python 3 Packages
Install pip `sudo apt-get install python3-pip`<br>
Install pymodbus `sudo pip3 install pymodbus`<br>
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)

## Server
Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)<br>
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)