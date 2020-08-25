# Installation
## OS
Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md <br>
* change password, connect to wifi, enable SSH, keyboard layout, set timezone, and any other necessry configurations.<br>
`sudo apt update`<br>
`sudo apt full-upgrade`

## Repository
`sudo apt-get install git`<br>
`git clone http://www.github.com/alexnathanson/solar-protocol`

## Python 3 Packages
Install pip `sudo apt-get install python3-pip`<br>
Install pymodbus `sudo pip3 install pymodbus`<br>
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)
Install numpy 'sudo pip3 uninstall numpy' followed by `sudo apt-get install python3-numpy `
## Server
Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)<br>
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)