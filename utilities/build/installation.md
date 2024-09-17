# Installation

Here are some manual steps after booting the raspberry pi to finnish installaion

## Create ssh key and connect to the pi

On your computer, generate a new key, with a new password

    ssh-keygen -f ~/.ssh/solar-protocol

Add the key to your keychain, using the password you just gave

    ssh-add ~/.ssh/solar-protocol

Install it to the raspberry pi - use the regular password

    ssh-copy-id -i ~/.ssh/solar-protocol pi@solar-protocol.local
    
Connect to the pi - there should be no password prompt here

    ssh pi@solar-protocol.local

Once connected, disable password authentication

    sudo ./disable-ssh-password-auth

## Secure firewall and website

Once you have confirmed that key authentication works over ssh, enable the firewall

    sudo ufw enable

Next, reach out to a network admin, who will follow the instructions in [network/ssl-management.md]() to add secure certificates for the website

## Join the network

Log in to the admin console via the browser [http://solar-protocol.local/admin]()

Enter API keys and update the gateway list with appropriate credentials

Enter your info on the settings page

## Forward ports from your router to the raspberry pi

Open and forward these ports on your router

* 443 -> 443 (https)
* 80 -> 80 (http)

If your home internet does not allow people to connect on ports 443 or 80, you can use these alternative ports

* 8443 -> 443 (alt-https)
* 8080 -> 80 (alt-http)
* 2222 -> 22 (For SSH)

## Congratulations

Give yourself a big hug!
