

# Installation

## Hardware

* Solar Charge Controller: We use EPever Tracer3210AN, but any Epever Tracer-AN Series would work.
* Raspberry Pi 3B+ or more recent

### Wiring
This works with a USB to RS485 converter (ch340T chip model).
* RJ45 blue => b
* RJ45 green => a

## Software

### OS
Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md <br>
* change password, connect to wifi, enable SSH, keyboard layout, set timezone, and any other necessry configurations.<br>
`sudo apt update`<br>
`sudo apt full-upgrade`

### Repository
`sudo apt-get install git`<br>
`git clone http://www.github.com/alexnathanson/solar-protocol`

### Python 3 Packages
Install pip `sudo apt-get install python3-pip`<br>
Install pymodbus `sudo pip3 install pymodbus`<br>
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)<br>
Install numpy 'sudo pip3 uninstall numpy' followed by `sudo apt-get install python3-numpy`

### Server
Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)<br>
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)<br>
Change Apache default directory to the frontend directory (src: https://julienrenaux.fr/2015/04/06/changing-apache2-document-root-in-ubuntu-14-x/)
* `cd /etc/apache2/sites-available`
* `sudo nano 000-default.conf`
* change `DocumentRoot /var/www/` to `DocumentRoot /home/pi/solar-protocol/frontend`
* `sudo nano /etc/apache2/apache2.conf`
* add these lines to the file<br>
`<Directory /home/pi/solar-protocol/frontend/>`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Options Indexes FollowSymLinks`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`AllowOverride None`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
`</Directory>`
* `sudo service apache2 restart`

### Automate

#### permissions
* make deviceList.json writable `sudo chmod a+w /home/pi/solar-protocol/backend/api/v1/deviceList.json`
* make update_ip2.sh executable `sudo chmod +x /home/pi/solar-protocol/backend/update_ip2.sh`
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/cc.sh`
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py`
#### timing
* run charge controller data logger on start up (src: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-3-systemd)
	* verify it works `sudo reboot`<br>
* `crontab -e`
	* run clientPostIP every 15 minutes `*/15 * * * * python3 /home/pi/solar-protocol/backend/api/clientPostIP.py`
	* run solarProtocol every 5 minutes `*/5 * * * * python3 /home/pi/solar-protocol/backend/api/solarProtocol.py`
	* reboot periodically

### Troubleshooting
* Run `python 3 /home/pi/solar-protocol/charge-controller/test.py` to test the connection between Pi and charge controller
* Run `ps -aux` to list running processes