# Installation instructions for RPi OS Bookworm

Major changes in this version 
* Bookworm requires the use of a venv when using pip.
* The 'wait for network at boot' option in raspi-config is no longer available.

## Hardware

* Solar Charge Controller: We use EPever Tracer2210AN, but any Epever Tracer-AN Series would work.
* Raspberry Pi 4 (or 3B+)

### Wiring
This works with a USB to RS485 converter (ch340T chip model).
* RJ45 blue => b
* RJ45 green => a

## Software

NOTE: The default admin user needs to be 'pi'

### OS
* In the Raspberry Pi disk imager, set user to 'sp', password, enable ssh, wifi network, etc
* Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md  
	* A reboot is generally required and happens automatically after exiting the raspi-config interface. If it isn't automatic, reboot with this command:`sudo reboot`
* `sudo apt-get update`  
* `sudo apt-get upgrade`

### Repository
Download repo into /home/sp
`sudo apt-get install git`  
`git clone http://www.github.com/alexnathanson/solar-protocol`  
* See below for updating server with local info and setting the appropriate security measures. 

### Create VENV

Navigate to the solar-protocol directory
`python3 -m venv .venv`

### Python 3 packages

from the solar-protocol directory
`source .venv/bin/activate`

<!-- try: `pip install -r requirements.txt` -->

if that fails, manually install all packages with these commands:

*************
#### Manual installation of packages (skip this section if previous step succeeds) 
* Install pymodbus `pip install pymodbus`
<!-- * Install pyserial `pip install pyserial` (probably not needed anymore) -->
* Install pandas `pip install pandas` (this should be refactored to not used pandas)   
* Install numpy `pip install numpy`
<!-- `sudo pip3 uninstall numpy` (might have already been installed) followed by `sudo apt-get install python3-numpy` (installing numpy with python3 can cause problems. see troubleshooting numpy below if this doesn't work)   -->
* Install jinja `pip install jinja2`     
<!-- * Upgrade pip: `python3 -m pip install --upgrade pip` -->
* Upgrade/install Pillow `pip install --upgrade Pillow`  
* Install cairo `sudo apt-get install libcairo2-dev`  
* Install gizeh `pip install gizeh`  
* Install webcolors `pip install webcolors`

#### Troubleshooting numpy
uninstall numpy (these uninstall commands may need to be run multiple times to get rid of multiple versions):
* `sudo pip3 uninstall numpy` and/or `sudo apt-get remove python3-numpy`
then install numpy and this missing library:
* `sudo pip3 install numpy`
* `sudo apt-get install libatlas-base-dev`

#### Troubleshooting PIL
* `sudo apt install libtiff5`
* `sudo apt-get install libopenjp2-7` (not confirmed)
* more PIL & Pillow troubleshooting at https://stackoverflow.com/questions/26505958/why-cant-python-import-image-from-pil

#### Troubleshoot pymodbus
* If you get an error relating to serial try removing serial and pyserial from all users and then reinstall only pyserial
	pip uninstall serial
	sudo pip uninstall serial
	pip uninstall pyserial
	sudo pip install pyserial

#### Further troubleshooting updates and dependencies
* In some instances it may be necessary to manually change the mirror which determines where apt-get pulls from. Instructions for manually changing the mirror can be found at https://pimylifeup.com/raspbian-repository-mirror/

### Security
Enable key-based authentication   
* run `install -d -m 700 ~/.ssh`  
* move the authorized_keys file into this new directory `sudo cp /home/pi/solar-protocol/utilities/authorized_keys ~/.ssh/authorized_keys`   
* set permissions. 
	* `sudo chmod 644 ~/.ssh/authorized_keys`  
	* `sudo chown pi:pi ~/.ssh/authorized_keys`  
* Enable rsa
	* `sudo nano /etc/ssh/sshd_config`
	* add this line `PubkeyAcceptedAlgorithms +ssh-rsa`
	* save the file and restart the service `sudo systemctl restart sshd`
* Test that passwordless key-based authentication works. 
* If it works, disable password login  
	* `sudo nano /etc/ssh/sshd_config`  
	* Change this line `#PasswordAuthentication yes` to `PasswordAuthentication no` (This will make it so you only can log in with the ssh key. Be careful to not lock yourself out!)  
	* save the file and restart the service `sudo systemctl restart sshd`

#### Firewall configuration 	

### Network Configuration & Server Setup
Open ports 80 and 22 on your router. It is strongly recommended to do this only after key-based authentication has been enabled and password authentication has be disabled.

Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)   
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)  
  

#### Configure Apache server
Change Apache default directory to the frontend directory (src: https://julienrenaux.fr/2015/04/06/changing-apache2-document-root-in-ubuntu-14-x/)  
  
* `sudo nano /etc/apache2/sites-available/000-default.conf`  
	* change `DocumentRoot /var/www/html` to `DocumentRoot /home/pi/solar-protocol/frontend`  
	* Enable server status interface (once enabled, the server stats page for an individual server will appear at solarprotocol.net/server-status (substitute IP address for individual servers). A machine readable version can be found at solarprotocol.net/server-status?auto )
		* add these 4 lines to the file directly above `</VirtualHost>`<br>
		`<Location /server-status>`<br>
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SetHandler server-status`<br>
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
		`</Location>`
		* save and close the file. Then restart service with `sudo service apache2 restart`
* `sudo nano /etc/apache2/apache2.conf`  
	* add these lines to the file    
	`<Directory /home/pi/solar-protocol/frontend/>`    
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Options Indexes FollowSymLinks`   
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`AllowOverride All`  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Header set Access-Control-Allow-Origin "*"`  
	`</Directory>`  
* To allow CORS (needed for admin console) activate module for changing headers. This can be done from any directory. `sudo a2enmod headers`  
* Enable URL rewrite module: `sudo a2enmod rewrite`
* Enable `sudo a2enmod userdir`
* Restart service with `sudo systemctl restart apache2`   

Apache permissions
* Add pi user to www-data group `sudo adduser pi www-data`
* Assign ownership of frontend directory to www-data group `sudo chown www-data:www-data /home/pi/solar-protocol/frontend`
* `sudo chmod 755 /home/pi/`

### Solar Protocol Configuration
Copy local directory outside of solar-protocol directory to pi directory  
`sudo cp -r /home/pi/solar-protocol/local /home/pi/local`
* Update the info with your information as needed  

Device List 
* change the device list template file name<br>
`sudo mv /home/pi/solar-protocol/backend/data/deviceListTemplate.json /home/pi/solar-protocol/backend/data/deviceList.json`

#### Permissions

All the necessary file and directory permissions can set by running this script: utilities/setAllPermissions.sh
* `sh setAllPermissions.sh`
* You must move the local directory to its proper position before setting permissions.
* If the above command was successful, you do not need to set permissions individually. If it failed or can't be run for some reason you can manually enter the commands listed in the setAllPermissions script.

### Automate  
<!-- open rc.local `sudo nano /etc/rc.local`  
* add this line above "exit 0" `sudo -H -u pi sh /home/pi/solar-protocol/start.sh > /home/pi/solar-protocol/start.log 2>&1 &`  
	* verify it works `sudo reboot` -->
* open rc.local `sudo nano /etc/rc.local`  
		* add this line above "exit 0" `sudo -H -u pi /bin/bash /home/pi/solar-protocol/backend/start.sh > /home/pi/solar-protocol/backend/start.log 2>&1 &`  


* open the root crontab `sudo crontab -e` and add this line to the bottom to restart the server at midnight:  
	* reboot daily `@midnight sudo reboot`

#### Automation Troubleshooting

* Confirm that "Wait for Network at Boot" option is enable. This ensures that the necessary network requirements are in place before Solar Protocol runs.  
* Confirm the python scripts are exectutable
* If you can't get the backend Python scripts to run from rc.local an alternative runner is provided. Change the rc.local line for the backend scripts to this:
	* open rc.local `sudo nano /etc/rc.local`  
		* add this line above "exit 0" `sudo -H -u pi sh /home/pi/solar-protocol/backend/alt-runner.sh > /home/pi/solar-protocol/backend/runner.log 2>&1 &`  

### General Troubleshooting  
* Run `python3 /home/pi/solar-protocol/charge-controller/test.py` to test the connection between Pi and charge controller  
* Run `ps -aux` to list running processes  
* Run `ps -ef | grep .py` to list running python processes
* All Python scripts use python3  
* if cron logging isn't working use `sudo crontab -e` instead of `crontab -e`  
* PHP error logging (best to only use these during development and revert back for production version)  
	* `sudo /etc/php/7.3/apache2/php.ini` The exact path will differ depending on the version of PHP  
	* Set display_errors and error_reporting as follows:  
		* `display_errors = On`   
		* `error_reporting = E_ALL`  
* point of contact logging only logs when it is TRUE. Uncomment out the logging for FALSE if you need to test out that it is logging these events.  
* Apache logs are found here: /var/log/apache2/access.log
	* Use `sudo tail -100 /var/log/apache2/access.log` to display the last 100 entries
	* More info on Apache logs can be found at https://phoenixnap.com/kb/apache-access-log
* The individual server status can be found at http://www.solarprotocol.net/server-status
	* append ?auto for machine readable version)
	* replace http://www.solarprotocol.net with whichever IP is needed

### Troubleshooting Opening Ports
* Log into the router and set a static internal IP
* Set up port forwarding for port 22 and 80 for the internal IP address
* In some places, ISPs blocks ports. Call them to check these ports arent blocked.
* Tool to check if ports are blocked: https://www.yougetsignal.com/tools/open-ports/
* Check firewall is off
* Try forwarding a port that is not port 80.

### Manually updating the software from the Repository  
* cd into the solar protocol folder and git pull  
	* `cd /home/pi/solar-protocol`  
	* `git pull`  
	* If you get any errors here, it is likely you have made some local changes to the code base that will give you a merge error. To deal with this run: `git stash` and then git pull again.   
* Update the permissions. cd into the utlitiles folder and run the setAllPermissions.sh script.   
	* `cd /home/pi/solar-protocol/utilities`  
	* `sh setAllPermissions.sh`  

* Update the public keys file on your pi. This is in case there have been changes to the public keys file. This allows some of the Solar Protocol developers access to your pi as needed.   
	* move the authorized_keys file into this new directory `sudo mv /home/pi/solar-protocol/utilities/authorized_keys ~/.ssh/authorized_keys`.    
