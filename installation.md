

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

### Security
Careful to set up pi securely.
* Check the password is secure
* Open ports 80 and 22 on your router. 
* Secure pi - here is a guide: https://www.raspberrypi.org/documentation/configuration/security.md
	* Block login to pi from root
    * Using key-based authentication.
    	* run `install -d -m 700 ~/.ssh`
    	* move the authorized_keys file into this new directory `sudo mv /home/pi/solar-protocol/utilities/authorized_keys ~/.ssh/authorized_keys`
    	* set permissions
    		* `sudo chmod 644 ~/.ssh/authorized_keys`
			* `sudo chown pi:pi ~/.ssh/authorized_keys`
		* test that passwordless key-based authentication works
		* if it works, disable password login
			* `sudo nano /etc/ssh/sshd_config`
			* change this line `#PasswordAuthentication yes` to `PasswordAuthentication no` (This will make it so you only can log in with the ssh key. Be careful to not lock yourself out!)
    * Installed firewall and fail2ban

### Repository
Download repo into /home/pi
`sudo apt-get install git`<br>
`git clone http://www.github.com/alexnathanson/solar-protocol`

### Python 3 Packages
Install pip `sudo apt-get install python3-pip`<br>
Install pymodbus `sudo pip3 install pymodbus`<br>
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)<br>
Install numpy 'sudo pip3 uninstall numpy' followed by `sudo apt-get install python3-numpy`<br>

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
* `sudo service apache2 restart`<br>
Allow CORS for admin console (optional: only needed if using admin console)
* activiate module for changing headers `sudo a2enmod headers`<br>
	`<Directory /home/pi/solar-protocol/frontend/admin/>`<br>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Header set Access-Control-Allow-Origin "*"`<br>
	`</Directory>`
* `sudo service apache2 restart`

### Automate

#### permissions
* `sudo chmod a+w /home/pi/solar-protocol/backend/api/v1/deviceList.json`
* `sudo chmod +x /home/pi/solar-protocol/backend/update_ip2.sh`
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py`

#### timing
* run charge controller data logger on start up (src: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup)
	* open rc.local `sudo nano /etc/rc.local`
		* add this line above "exit 0" `sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &`
	* verify it works `sudo reboot`
* open crontab `sudo crontab -e` and add these lines to the bottom:
	* run clientPostIP every 15 minutes `*/15 * * * * /usr/bin/python3 /home/pi/solar-protocol/backend/api/v1/clientPostIP.py > /home/pi/solar-protocol/backend/api/v1/clientPostIP.log 2>&1`
	* run solarProtocol every 5 minutes `*/5 * * * * /usr/bin/python3 /home/pi/solar-protocol/backend/api/v1/solarProtocol.py > /home/pi/solar-protocol/backend/api/v1/solarProtocol.log 2>&1`
	* reboot daily `@midnight sudo reboot`	

### Troubleshooting
* Run `python3 /home/pi/solar-protocol/charge-controller/test.py` to test the connection between Pi and charge controller
* Run `ps -aux` to list running processes
* All Python scripts use python3
* if cron logging isn't working use `sudo crontab -e` instead of `crontab -e`