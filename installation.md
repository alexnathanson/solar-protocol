# Software Installation Instructions for Solar Protocol V1.1 for RPi OS Bookworm

These are the installation instructions for the current version of Solar Protocol that runs on Bookworm.

Major changes in this version 
* All python scripts now run in a virtual environment.

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
* In the Raspberry Pi disk imager, set user to 'pi', password, enable ssh, wifi network, etc
* Configure device `sudo raspi-config` https://www.raspberrypi.org/documentation/configuration/raspi-config.md
	* Set locale to en_US.UTF-8 (The default of en_US may throw an error.)
	* A reboot is generally required and happens automatically after exiting the raspi-config interface. If it isn't automatic, reboot with this command:`sudo reboot`
* `sudo apt-get update`  
* `sudo apt-get upgrade`

### Repository
Download repo into /home/pi
`sudo apt-get install git`  
`git clone http://www.github.com/alexnathanson/solar-protocol`  

### Create VENV

Navigate to the solar-protocol directory
`python3 -m venv .venv`

### Python 3 packages

From the /home/pi/solar-protocol directory, activate the virtual environment
`source .venv/bin/activate`

Try `pip install -r requirements.txt`

If that fails, manually install all packages with these commands:

#### Manual installation of packages (skip this section if previous step succeeds) 
* Install requets `pip install requests`
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

### Network Configuration & Server Setup
Open and forward these ports:
* 80 -> 80 (This is to catch external traffic coming in on port 80. It could probably forward to the internal port 80 just fine too)
* 8080 -> 8080 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 80.)
* 443 -> 443 (For HTTPS)
* 8443 -> 443 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 443.)
* 2222 -> 22 (For SSH)

It is strongly recommended to do this only after key-based authentication has been enabled and password authentication has be disabled.

Install Apache `sudo apt-get install apache2 -y`

Install PHP `sudo apt-get install php -y`
  
#### Configure Apache server
Change Apache default directory to the frontend directory and set permissions
* `sudo nano /etc/apache2/sites-available/000-default.conf`  
	* change `<VirtualHost *:80>` to `<VirtualHost *:80 *:8080>` 
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
* Add port 8080 to ports.conf
	* `sudo nano /etc/apache2/ports.conf`
	* Add this line: `Listen 8080`
* To allow CORS (needed for admin console) activate module for changing headers. This can be done from any directory. `sudo a2enmod headers`  
* Enable URL rewrite module: `sudo a2enmod rewrite`
* Enable `sudo a2enmod userdir`
* Restart service with `sudo systemctl restart apache2`   

Apache permissions
* Add pi user to www-data group `sudo adduser pi www-data`
* Assign ownership of frontend directory to www-data group `sudo chown www-data:www-data /home/pi/solar-protocol/frontend`
* `sudo chmod 755 /home/pi/`

#### SSL Certificate Setup
Port forwarding for 443-> 443 must be enabled for this to take effect (8443 -> 443 must also be enabled on some routers to minimize troubleshooting issues).

1) `sudo apt install python3-certbot-apache`
2) `sudo apt install certbot`
3) `a2enmod ssl`
4) Solar Protocol uses a single certificate distributed to all SP servers. The next steps must be done by a network admin. (See network/ssl-management.md for more info.)

#### PHP Settings (Note: adding this my be a sympton of other issues.)
Set timezone (Change 8.2 to your version of PHP if needed)
* `sudo nano /etc/php/8.2/apache2/php.ini`
* Change `;date.timezone` to `date.timezone = YOUR_TIMEZONE`
	* You can find your timezone here: https://www.php.net/manual/en/timezones.america.php
* `sudo systemctl restart apache2` for this change to take effect

#### Install Fail2Ban
Fail2ban provides added protection against bot attacks.
* For the time being use these instructions: https://pimylifeup.com/raspberry-pi-fail2ban/ Solar Protocol specific instructions may be provided in the future.

* Install Fail2ban: `sudo apt install fail2ban`
* Copy the config file: `sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local`
* Open it in an editor: `sudo nano /etc/fail2ban/jail.local`
* Press control + w, type `sshd`, then press enter, to search for the SSH section. You want to locate the `[sshd]` section under the heading JAILS. (Every time you search it finds the next instance, so you may need to do it a couple of times.)
* Under the `[sshd]` section add these lines. Uncomment [sshd] if its commented out.
```
[sshd]

enabled = true
port = ssh
backend = systemd
logpath = /var/log/auth.log
maxretry = 5
bantime = 3600
```
* Restart the service: `sudo systemctl restart fail2ban`
* Check the status to ensure its active: `/etc/init.d/fail2ban status`

### Solar Protocol Configuration
1) Copy local directory outside of solar-protocol directory to pi directory

`sudo cp -r /home/pi/solar-protocol/local /home/pi/local`

2) Change the device list template file name

`sudo mv /home/pi/solar-protocol/backend/data/deviceListTemplate.json /home/pi/solar-protocol/backend/data/deviceList.json`

3) Set permissions (this script needs to be run everytime you pull from the repository)

`sh /home/pi/solar-protocol/utilities/setAllPermissions.sh`

If the above command was successful, you do not need to set permissions individually. If it failed or can't be run for some reason you can manually enter the commands listed in the setAllPermissions script.

4) Log in to the admin console via the browser (YOUR_IP/admin)
* Enter your info on the settings page
* Enter API keys and update the gateway list with appropriate credentials

### Automate  

Install system service so that solar-protocol runs every time the pi is powered on

    bash development/scripts/install-system-service
		
Restart the system on midnight each day

    sudo crontab -e

Add this line to the bottom to restart the server at midnight

    @midnight sudo reboot

## Troubleshooting  
* Check the service status with `systemctl status solar-protocol`
* Look at the logs with `journalctl -u solar-protocol`
* Run `python3 /home/pi/solar-protocol/charge-controller/test.py` to test the connection between Pi and charge controller  
* Run `ps -aux` to list running processes  
* Run `ps -ef | grep .py` or `ps aux | grep .py` to list running python processes
* All Python scripts use python3  
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
* ISPs can blocks ports. Call your ISP to check that these ports arent blocked.
* On many residential networks, internal loopbacks on ports 80 and 443 can be blocked. You can test this by using a different network (like cellular) to try to access the site.
* There are tools to check if ports are open or closed. They aren't always accurate. Here's one: https://www.yougetsignal.com/tools/open-ports/
* Try ports 8080 and 8443, instead of 80 and 443.

### Manually updating the software from the Repository  
* cd into the solar protocol folder and git pull  
	* `cd /home/pi/solar-protocol`  
	* `git pull`  
	* If you get any errors here, it is likely you have made some local changes to the code base that will give you a merge error. To deal with this run: `git stash` and then git pull again.   
* Update the permissions. cd into the utlitiles folder and run the setAllPermissions.sh script.   
	* `cd /home/pi/solar-protocol/utilities`  
	* `sh setAllPermissions.sh`  
