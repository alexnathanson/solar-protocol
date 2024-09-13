# Installation

Here are some manual steps after booting the raspberry pi to finnish installaion

Update the password for the `pi` user

    passwd

- [ ] add 8080 and 8443 to apache
- [ ] setup ssl
- [ ] enter api keys
- [ ] edit admin settings

## Configure Apache server

Add port 8080 to the server config

Change `<VirtualHost *:80>` to `<VirtualHost *:80 *:8080>` in **/etc/apache2/sites-available/000-default.conf**

		sudo nano /etc/apache2/sites-available/000-default.conf

Add `Listen 8080` to the end of **/etc/apache2/ports.conf**

		sudo nano /etc/apache2/ports.conf`

## Forward ports from your router to the raspberry pi

It is strongly recommended to do this only after key-based authentication has been enabled and password authentication has be disabled.

Open and forward these ports on your router

* 80 -> 80 (This is to catch external traffic coming in on port 80. It could probably forward to the internal port 80 just fine too)
* 443 -> 443 (For HTTPS)

* 8080 -> 8080 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 80.)
* 8443 -> 443 (Alt-HTTP... Many residential networks have internal loopback prohibitions on port 443.)
* 2222 -> 22 (For SSH)

## Add SSL Certificates

Reach out to a network admin, who will follow the instructions in [network/ssl-management.md]()

## Fix permissions

Set permissions for all files - this script must be run everytime you pull from the repository

    sh /home/pi/solar-protocol/utilities/setAllPermissions.sh

## Join the network

Enter api keys to join the network 

Log in to the admin console via the browser [http://solar-protocol.local/admin]()

Enter API keys and update the gateway list with appropriate credentials

Enter your info on the settings page

## Congratulations

Give yourself a big hug!
