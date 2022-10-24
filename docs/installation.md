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

Reboot the pi

    sudo reboot

### Code

Download the git repo into /home/pi

    sudo apt-get install git --yes
    git clone http://www.github.com/alexnathanson/solar-protocol

Install required dependencies

    bash /home/pi/solar-protocol/dev/install.sh

### Security

Recommendations to set up your pi securely

* Choose a strong password  
* Open ports 80 and 22 on your router    
* Following [the raspberry pi security guide](https://www.raspberrypi.org/documentation/configuration/security.md)

Test that it works by ssh'ing in from another terminal. If it works, disable password login

**! This will make it so you only can log in with the ssh key. Be careful to not lock yourself out!**

    sed --in-place --expression \
      's/#PasswordAuthentication yes/PasswordAuthentication no/' \
      /etc/ssh/sshd_config

#### reboot at midnight

Open the root crontab

    sudo crontab -e

Add this line to the bottom to restart the server at midnight

    reboot daily `@midnight sudo reboot`

#### Automation Troubleshooting

- [] Confirm that "Wait for Network at Boot" option in `raspi-config` is enabled. This ensures that the necessary network requirements are in place before Solar Protocol runs.  

### General Troubleshooting  

- [] Test the connection between the pi and charge controller

    python3 /home/pi/solar-protocol/dev/test-charge-controller-connection.py

- [] List running services

    ./solar-protocol status

- [] If cron logging isn't working, use `sudo crontab -e` instead of `crontab -e`  

- [] Point of contact logging only logs when it is TRUE. Uncomment out the logging for FALSE if you need to test out that it is logging these events.  

- [] Check the last 100 nginx log entries 
	
    sudo tail -100 /var/log/nginx/access.log

- [] Check the last 100 nginx error log entries 

    sudo tail -100 /var/log/nginx/error.log

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
