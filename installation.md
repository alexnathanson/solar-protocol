

# Installation

## Hardware

* Solar Charge Controller: We use EPever Tracer2210AN, but any Epever Tracer-AN Series would work.
* Raspberry Pi 4 (or 3B+)

### Wiring
This works with a USB to RS485 converter (ch340T chip model).
* RJ45 blue => b
* RJ45 green => a

## Software

### OS
* Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md  
	* change password, hostname, connect to wifi, enable SSH, keyboard layout, set timezone, and any other necessry configurations
	* Enable "Wait for Network at Boot" option. This ensures that the necessary network requirements are in place before Solar Protocol runs.  
	* A reboot is generally required and happens automatically after exiting the raspi-config interface. If it isn't automatic, reboot with this command:`sudo reboot` 
* `sudo apt-get update`  
* `sudo apt full-upgrade` (note that `sudo apt-get upgrade`  is the "safer" version of this command that is probably better to use if an upgrade is necessary after Solar Protocol is installed and running in order to avoid problems with dependencies)

### Repository
Download repo into /home/pi
`sudo apt-get install git`  
`git clone http://www.github.com/alexnathanson/solar-protocol`  
* See below for updating server with local info and setting the appropriate security measures. 

### Python 3 Packages  
* Install pip `sudo apt-get install python3-pip`  
* Install pymodbus `sudo pip3 install pymodbus`    
* Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)   
* Install numpy `sudo pip3 uninstall numpy` (might have already been installed) followed by `sudo apt-get install python3-numpy` (installing numpy with python3 can cause problems. see troubleshooting numpy below if this doesn't work)  
* Install jinja `sudo pip3 install jinja2`     

#### Python 3 Packages for the visualization
* Upgrade pip: `python3 -m pip install --upgrade pip`
* Upgrade/install Pillow `python3 -m pip install --upgrade Pillow`  
* Install cairo `sudo apt-get install libcairo2-dev`  
* Install gizeh `sudo pip3 install gizeh`  
* Install webcolors `sudo pip3 install webcolors`  

#### Troubleshooting numpy
uninstall numpy (these uninstall commands may need to be run multiple times to get rid of multiple versions):
* `sudo pip3 uninstall numpy` and/or `sudo apt-get remove python3-numpy`
then install numpy and this missing library:
* `sudo pip3 install numpy`
* `sudo apt-get install libatlas-base-dev`

#### Troubleshooting PIL
* 'sudo apt install libtiff5'

#### Further troubleshooting updates and dependencies
* In some instances it may be necessary to manually change the mirror which determines where apt-get pulls from. Instructions for manually changing the mirror can be found at https://pimylifeup.com/raspbian-repository-mirror/

### Security
Recommendations to set up your pi securely   
* Choose a strong password  
* Open ports 80 and 22 on your router    
* Secure pi - here is a guide: https://www.raspberrypi.org/documentation/configuration/security.md  
    * To use key-based authentication   
    	* run `install -d -m 700 ~/.ssh`  
    	(to be performed after downloading the solar-protocol repo) 
	* move the authorized_keys file into this new directory `sudo mv /home/pi/solar-protocol/utilities/authorized_keys ~/.ssh/authorized_keys`   
    	* set permissions. 
    		* `sudo chmod 644 ~/.ssh/authorized_keys`  
			* `sudo chown pi:pi ~/.ssh/authorized_keys`  
		* test that passwordless key-based authentication works. 
		* if it works, disable password login  
			* `sudo nano /etc/ssh/sshd_config`  
			* change this line `#PasswordAuthentication yes` to `PasswordAuthentication no` (This will make it so you only can log in with the ssh key. Be careful to not lock yourself out!)  

### Server
Install Apache `sudo apt-get install apache2 -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/2)   
Install PHP `sudo apt-get install php -y` (https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/3)    
  

Change Apache default directory to the frontend directory (src: https://julienrenaux.fr/2015/04/06/changing-apache2-document-root-in-ubuntu-14-x/)  
  
* `cd /etc/apache2/sites-available`  
* `sudo nano 000-default.conf`  
	* change `DocumentRoot /var/www/` to `DocumentRoot /home/pi/solar-protocol/frontend`  
* `sudo nano /etc/apache2/apache2.conf`  
	* add these lines to the file    
	`<Directory /home/pi/solar-protocol/frontend/>`    
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Options Indexes FollowSymLinks`   
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`AllowOverride All`  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Header set Access-Control-Allow-Origin "*"`  
	`</Directory>`  
* To allow CORS (needed for admin console) activate module for changing headers. This can be done from any directory. `sudo a2enmod headers`  

To allow for htaccess redirect activate this module: `sudo a2enmod rewrite`
* then restart `sudo systemctl restart apache2`   

Enable server status interface:
* edit the 000-default.conf file: `sudo nano /etc/apache2/sites-enabled/000-default.conf`
* add these 4 lines to the file directly above `</VirtualHost>`<br>
`<Location /server-status>`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`SetHandler server-status`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
`</Location>`
* save and close the file. Then restart with `sudo service apache2 restart` (if this restart command doesn't work, use the Apache resart command mention above)
* once enabled, the server stats page for an individual server will appear at solarprotocol.net/server-status (substitute IP address for individual servers). A machine readable version can be found at solarprotocol.net/server-status?auto

Install PHP graphics library for dithering. Note that the version will need to match your php version.
* `sudo apt-get install php7.3-gd`
* `sudo systemctl restart apache2`   
<!-- 
Give Apache/PHP user 'www-data' necessary permissions:
* Open visudo: `sudo visudo`
* Add this line to the bottom of the file: `www-data	ALL=NOPASSWD: ALL`
 -->

### Local
* Move local directory outside of solar-protocol directory to pi directory  
`sudo mv /home/pi/solar-protocol/local /home/pi/`
* Update the info with your information as needed  

### Permissions

All the necessary file and directory permissions can set by running this script: utilities/setAllPermissions.sh
* `sh setAllPermissions.sh`
* You must move the local directory to its proper position before setting permissions.

If you need to set permissions individually 
* `sudo chmod a+w /home/pi/local/.spenv`
* `sudo chmod a+w /home/pi/local/local.json`
* `sudo chmod a+w /home/pi/local/access.json`
* `sudo chmod -R a+w /home/pi/local/www`
* `sudo chmod a+w /home/pi/solar-protocol/backend/data/deviceList.json`
* `sudo chmod a+w /home/pi/solar-protocol/backend/data/poe.log`
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py`
* `sudo chmod a+w /home/pi/solar-protocol/frontend/index.html`
* `sudo chmod +x /home/pi/solar-protocol/utilities/update.sh`
* `sudo chmod a+w /home/pi/solar-protocol/frontend/images/clock-exhibit.png`

### Automate  

* run charge controller data logger on start up (src: https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup)
	* open rc.local `sudo nano /etc/rc.local`  
		* add this line above "exit 0" `sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &`  
	* verify it works `sudo reboot`  
* run Python script runner on start up
	* open rc.local `sudo nano /etc/rc.local`  
		* add this line above "exit 0" `sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/backend > /home/pi/solar-protocol/backend/runner.log 2>&1 &`  
	* verify it works `sudo reboot`  	
* open the root crontab `sudo crontab -e` and add this line to the bottom to restart the server at midnight:  
	* reboot daily `@midnight sudo reboot`

### Troubleshooting  
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
