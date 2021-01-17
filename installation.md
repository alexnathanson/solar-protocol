

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

### Repository
Download repo into /home/pi
`sudo apt-get install git`<br>
`git clone http://www.github.com/alexnathanson/solar-protocol`<br>
* See below for updating server with local info

### Python 3 Packages
Install pip `sudo apt-get install python3-pip`<br>
Install pymodbus `sudo pip3 install pymodbus`<br>
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)<br>
Install numpy 'sudo pip3 uninstall numpy' followed by `sudo apt-get install python3-numpy`<br>
Install jinja 'sudo pip3 install jinja2' <br>

### Server
Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)<br>
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)<br>

<p>
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
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Header set Access-Control-Allow-Origin "*"`<br>
	`</Directory>`
* To allow CORS (needed for admin console) activate module for changing headers. This can be done from any directory. `sudo a2enmod headers`
* `sudo service apache2 restart`
</p>

### Automate

#### permissions (you can set all these permissions at once via the utilities/setAllPermissions.sh script if you want)
* `sudo chmod a+w /home/pi/solar-protocol/backend/api/v1/deviceList.json`
* `sudo chmod +x /home/pi/solar-protocol/backend/update_ip2.sh`
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py`
* `sudo chmod a+w /home/pi/solar-protocol/frontend/index.html`

#### timing
* run charge controller data logger on start up (src: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup)
	* open rc.local `sudo nano /etc/rc.local`
		* add this line above "exit 0" `sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &`
	* verify it works `sudo reboot`
* open the root crontab `sudo crontab -e` and add these lines to the bottom:
	* run clientPostIP every 15 minutes `*/15 * * * * /usr/bin/python3 /home/pi/solar-protocol/backend/api/v1/clientPostIP.py > /home/pi/solar-protocol/backend/api/v1/clientPostIP.log 2>&1`
	* run solarProtocol every 5 minutes `*/5 * * * * /usr/bin/python3 /home/pi/solar-protocol/backend/api/v1/solarProtocol.py > /home/pi/solar-protocol/backend/api/v1/solarProtocol.log 2>&1`
	* run createHTML every 15 minutes to generate new index.html with current data. `*/15 * * * * cd /home/pi/solar-protocol/backend/createHTML && $(which python3) create_html.py`
	* reboot daily `@midnight sudo reboot`	
* open the crontab for the user `crontab -e` and add this line to the bottom: 
	* on reboot, run the update script to check from updates from github. '@reboot sh /home/pi/solar-protocol/utilities/update.sh'

### Local
* Move local directory outside of solar-protocol directory to pi directory
* Update the info with your information as needed

### Troubleshooting
* Run `python3 /home/pi/solar-protocol/charge-controller/test.py` to test the connection between Pi and charge controller
* Run `ps -aux` to list running processes
* All Python scripts use python3
* if cron logging isn't working use `sudo crontab -e` instead of `crontab -e`
* PHP error logging (best to only use these during development and revert back for production version)
	* `sudo /etc/php/7.3/apache2/php.ini` The exact path will differ depending on the version of PHP
	* Set display_errors and error_reporting as follows:
		* `display_errors = On`
		* `error_reporting = E_ALL`
* point of contact logging only logs when it is TRUE. Uncomment out the logging for FALSE if you need to test out that it is logging these events.
