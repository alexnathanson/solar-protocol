# todo

- [ ] open firewall (ufw allow http/https)
  - [ ] maybe can set as service that depends on userinfo service
- [ ] add 8080 and 8443 to apache
- [ ] setup ssl
- [ ] enter api keys
- [ ] edit admin settings
- [ ] first boot DO NOT RENAME pi user but DO give a different password

### Network Configuration & Server Setup

    sudo ufw allow http
    sudo ufw allow https

It is strongly recommended to do this only after key-based authentication has been enabled and password authentication has be disabled.

Open and forward these ports:
* 80 -> 80 (This is to catch external traffic coming in on port 80. It could probably forward to the internal port 80 just fine too)
* 443 -> 443 (For HTTPS)

* 8080 -> 8080 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 80.)
* 8443 -> 443 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 443.)
* 2222 -> 22 (For SSH)

#### Configure Apache server

Change Apache default directory to the frontend directory and set permissions
* `sudo nano /etc/apache2/sites-available/000-default.conf`  
	* change `<VirtualHost *:80>` to `<VirtualHost *:80 *:8080>` 
* Add port 8080 to ports.conf
	* `sudo nano /etc/apache2/ports.conf`
	* Add this line: `Listen 8080`

#### SSL Certificate Setup
Port forwarding for 443-> 443 must be enabled for this to take effect (8443 -> 443 must also be enabled on some routers to minimize troubleshooting issues).

Solar Protocol uses a single certificate distributed to all SP servers. The next steps must be done by a network admin. (See network/ssl-management.md for more info.)

### Solar Protocol Configuration

1. Set permissions (this script needs to be run everytime you pull from the repository)

    sh /home/pi/solar-protocol/utilities/setAllPermissions.sh

If the above command was successful, you do not need to set permissions individually. If it failed or can't be run for some reason you can manually enter the commands listed in the setAllPermissions script.

2. Enter api keys to join the network 

Log in to the admin console via the browser (http://solar-protocol.local/admin)
* Enter your info on the settings page
* Enter API keys and update the gateway list with appropriate credentials

### troubleshooting

#### troubleshooting python - manual install

		pip install requests
		pip install pymodbus
		pip install pandas # (this should be refactored to not used pandas)  
		pip install numpy
		pip install jinja2
		pip install --upgrade Pillow
		sudo apt-get install libcairo2-dev
		pip install gizeh
		pip install webcolors

#### troubleshooting numpy - reinstall

		sudo pip3 uninstall numpy
		sudo apt-get remove python3-numpy
		sudo pip3 install numpy
		sudo apt-get install libatlas-base-dev

#### troubleshooting PIL

		sudo apt install libtiff5
		sudo apt-get install libopenjp2-7 # (unconfirmed)

#### troubleshoot pymodbus - reinstall

		pip uninstall serial
		sudo pip uninstall serial
		pip uninstall pyserial
		sudo pip install pyserial
