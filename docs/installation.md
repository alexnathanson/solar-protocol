# Installation

These are the original installation instructions. The [automated installer](../utilities/installer.sh) is untested and should not be used yet.

## Hardware

* Solar Charge Controller: We use [EPever Tracer2210AN](https://www.epever.com/product/tracer-an-10-40a-mppt-charge-controller/), but any Epever Tracer-AN Series would work.
* Raspberry Pi 4 (or 3B+)

### Wiring

This works with a [USB to RS485 converter](https://www.sparkfun.com/products/15938) (ch340T chip model).

* RJ45 blue => b
* RJ45 green => a

## Software

### OS

We use the official Raspberry Pi OS

Configure device with `sudo raspi-config` [raspi-config docs](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)
  * change password
  * set hostname
  * connect to wifi
  * enable SSH
  * set keyboard layout
  * set timezone, and any other necessry configurations
  * Enable "Wait for Network at Boot" option. This ensures that the necessary network requirements are in place before Solar Protocol runs.  

Reboot the pi with `sudo reboot`

Update the pi with `sudo apt update && sudo apt full-upgrade)

> Note that `sudo apt-get upgrade` is the "safer" version of full-upgrade that is probably better to use if an upgrade is necessary after Solar Protocol is installed and running in order to avoid problems with dependencies.

### Code

Download the git repo into /home/pi

    sudo apt install git
    git clone http://www.github.com/alexnathanson/solar-protocol

Install required frontend packages

    sudo apt install libcairo2-dev

Install pip, which manages python packages 

    sudo apt-get install python3-pip

Install required backend python packages

    cd ~/solar-protocol
    sudo pip3 install --requirement requirements.txt


#### Troubleshooting numpy
If there is an issue with numpy, try the following

    sudo pip3 uninstall numpy
    sudo apt install libatlas-base-dev
    sudo pip3 install numpy

#### Troubleshooting PILLOW

If there is an error with pillow, try

    sudo apt install libtiff5

#### Further troubleshooting updates and dependencies

In some instances it may be necessary to manually change the mirror which determines where apt pulls from. Instructions for manually changing the mirror can be found at https://pimylifeup.com/raspbian-repository-mirror/

### Security

Recommendations to set up your pi securely

* Choose a strong password  
* Open ports 80 and 22 on your router    
* Following [the raspberry pi security guide](https://www.raspberrypi.org/documentation/configuration/security.md)

Use key-based authentication:

    install -d -m 700 ~/.ssh

Add our authorized ssh keys

    sudo mv /home/pi/solar-protocol/utilities/authorized_keys /home/pi/.ssh/authorized_keys
    sudo chmod 644 /home/pi/.ssh/authorized_keys
    sudo chown pi:pi /home/pi/.ssh/authorized_keys

Test that it works by ssh'ing in from another terminal. If it works, disable password login

**! This will make it so you only can log in with the ssh key. Be careful to not lock yourself out!**

    sed --in-place --expression 's/#PasswordAuthentication yes/PasswordAuthentication no/' \
      /etc/ssh/sshd_config

### Server

Install Apache and PHP

    sudo apt install apache2 php --yes
  
Change Apache default directory to the frontend directory [src](https://julienrenaux.fr/2015/04/06/changing-apache2-document-root-in-ubuntu-14-x/)

    sudo nano /etc/apache2/sites-available/000-default.conf
  
change `DocumentRoot /var/www/` to `DocumentRoot /home/pi/solar-protocol/frontend`  


Set the directory options

    sudo nano /etc/apache2/apache2.conf

Add these lines to the file    

	<Directory /home/pi/solar-protocol/frontend/>
	    Options Indexes FollowSymLinks
	    AllowOverride All
	    Require all granted
	    Header set Access-Control-Allow-Origin "*"
	</Directory>

Activate CORS for apache (needed for admin console)

    sudo a2enmod headers

To allow for htaccess redirect activate this module

    sudo a2enmod rewrite

Enable server status interface

    sudo nano /etc/apache2/sites-enabled/000-default.conf

Add these 4 lines to the file directly above `</VirtualHost>`

    <Location /server-status>
        SetHandler server-status
        Require all granted
    </Location>`

The server status page for an individual server will appear at solarprotocol.net/server-status (substitute IP address for individual servers). A machine readable version can be found at solarprotocol.net/server-status?auto

Install PHP graphics library for dithering. Note that the version will need to match your php version.

    sudo apt install php-gd

Restart apache

    sudo service apache2 restart

### Local

Copy local directory outside of solar-protocol directory to pi directory  

    sudo cp -r /home/pi/solar-protocol/local /home/pi/local

Update the info with your information as needed

### Automation

#### Charge controller data logger

Run charge controller data logger on start up [src](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup)

    sudo nano /etc/rc.local

Add this line above "exit 0"

    sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/charge-controller/csv_datalogger.py > /home/pi/solar-protocol/charge-controller/datalogger.log 2>&1 &

Verify it works after rebooting with `sudo reboot`  


#### script runner

The script runner keeps the server up to date with the solar protocol network

    sudo nano /etc/rc.local

Add this line above "exit 0"

    sudo -H -u pi /usr/bin/python3 /home/pi/solar-protocol/backend > /home/pi/solar-protocol/backend/runner.log 2>&1 &

Verify it works after rebooting with `sudo reboot`  

#### reboot at midnight

Open the root crontab

    sudo crontab -e

Add this line to the bottom to restart the server at midnight

    reboot daily `@midnight sudo reboot`

#### Automation Troubleshooting

- [] Confirm that "Wait for Network at Boot" option in `raspi-config` is enabled. This ensures that the necessary network requirements are in place before Solar Protocol runs.  
- [] Confirm the python scripts are exectutable
- [] If you cannot get the backend Python scripts to run from rc.local an alternative runner is provided. Change the rc.local line for the backend scripts to this:

    sudo -H -u pi sh /home/pi/solar-protocol/backend/alt-runner.sh > /home/pi/solar-protocol/backend/runner.log 2>&1 &

### General Troubleshooting  

- [] Test the connection between the pi and charge controller

    python3 /home/pi/solar-protocol/charge-controller/test.py

- [] List running processes

    ps -aux

- [] List running python processes

    ps -ed | grep .py

- [] Confirm all Python scripts use python3  

- [] If cron logging isn't working, use `sudo crontab -e` instead of `crontab -e`  

- [] Enable PHP error logging (best to only use these during development and revert back for production version)

    sudo nano /etc/php/7.3/apache2/php.ini # The exact path will differ depending on the version of PHP  

Set display_errors and error_reporting as follows:

    display_errors = On
    error_reporting = E_ALL

- [] Point of contact logging only logs when it is TRUE. Uncomment out the logging for FALSE if you need to test out that it is logging these events.  

- [] Check the last 100 Apache log entries ([documentation on reading logs](https://phoenixnap.com/kb/apache-access-log))
	
    sudo tail -100 /var/log/apache2/access.log

- [] Check an individual server's status by visiting http://www.solarprotocol.net/server-status

    * append ?auto for machine readable version
    * replace http://www.solarprotocol.net with whichever IP is needed

### Troubleshooting Opening Ports

* Log into the router and set a static internal IP
* Set up port forwarding for port 22 and 80 for the internal IP address
* In some places, ISPs blocks ports. Call them to check these ports arent blocked.
* Tool to check if ports are blocked: https://www.yougetsignal.com/tools/open-ports/
* Check firewall is off
* Try forwarding a port that is not port 80.

### Manually updating the software from the Repository  

Get the latest code

 
    cd /home/pi/solar-protocol
    git pull

If you get any errors here, it is likely you have made some local changes to the code base that will give you a merge error. If that is the case, try the following:

    git stash
    git pull
    git stash pop # try and re-apply your local changes. This may break things further. If so, run `git stash` again.

Update the public keys file on your pi. This is in case there have been changes to the public keys file. This allows some of the Solar Protocol developers access to your pi as needed.

    sudo mv /home/pi/solar-protocol/utilities/authorized_keys /home/pi/.ssh/authorized_keys
    sudo chmod 644 /home/pi/.ssh/authorized_keys
    sudo chown pi:pi /home/pi/.ssh/authorized_keys
