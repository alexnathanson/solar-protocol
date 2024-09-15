# Installation

Here are some manual steps after booting the raspberry pi to finnish installaion

Update the password for the `pi` user

    passwd

## Enable firewal

This will make sure people can only access the website

    sudo ufw allow ssh
    sudo ufw allow http comment "Solar Protocol"
    sudo ufw allow http-alt comment "Solar Protocol (alt)"
    sudo ufw allow https comment "Solar Protocol"
    sudo ufw allow 8443 comment "Solar Protocol (alt)"
    sudo ufw enable
    sudo ufw status

## Forward ports from your router to the raspberry pi

It is strongly recommended to do this only after key-based authentication has been enabled and password authentication has be disabled.

Open and forward these ports on your router

* 443 -> 443 (https)
* 80 -> 80 (http)

If your home internet does not allow people to connect on ports 443 or 80, you can use these alternative ports

* 8443 -> 443 (alt-https)
* 8080 -> 80 (alt-http)
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
