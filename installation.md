

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
Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md  
* change password, hostname, connect to wifi, enable SSH, keyboard layout, set timezone, and any other necessry configurations    
* `sudo reboot` 
* `sudo apt-get update`  
* `sudo apt-get upgrade`  
or `sudo apt full-upgrade` 

### Repository
Download repo into /home/pi
`sudo apt-get install git`  
`git clone http://www.github.com/alexnathanson/solar-protocol`  
* See below for updating server with local info and setting the appropriate security measures. 

### Python 3 Packages  
Install pip `sudo apt-get install python3-pip`  
Install pymodbus `sudo pip3 install pymodbus`    
Install pandas `sudo pip3 install pandas` (this should be refactored to not used pandas)  
Install numpy `sudo pip3 uninstall numpy` (might have already been installed) followed by `sudo apt-get install python3-numpy`  
Install jinja `sudo pip3 install jinja2`    

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
* To allow for htaccess redirect activate this module: `sudo a2enmod rewrite`
* `sudo systemctl restart apache2`   

### Automate  

#### permissions (you can set all these permissions at once via the utilities/setAllPermissions.sh script by `sh setAllPermissions.sh`)  
* `sudo chmod a+w /home/pi/local/local.json` (You must move the local directory before setting permissions. See below.)
* `sudo chmod a+w /home/pi/solar-protocol/backend/api/v1/deviceList.json`  
* `sudo chmod +x /home/pi/solar-protocol/backend/update_ip2.sh`  
* `sudo chmod +x /home/pi/solar-protocol/charge-controller/csv_datalogger.py`  
* `sudo chmod a+w /home/pi/solar-protocol/frontend/index.html`  

#### Timing
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
	* on reboot, run the update script to check from updates from github. `@reboot sh /home/pi/solar-protocol/utilities/update.sh`  

### Local
* Move local directory outside of solar-protocol directory to pi directory  
`sudo mv /home/pi/solar-protocol/local /home/pi/`
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
