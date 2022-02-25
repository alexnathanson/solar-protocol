# Installation for Certbot

## links

https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal

https://peppe8o.com/use-lets-encrypt-and-certbot-to-secure-raspberry-pi-hosted-websites-automatically/



## Instructions

### Setup

`sudo apt update -y && sudo apt upgrade -y`

In order for the automated process to work, we need to explicitly create a virtual host file. (The default is that we direct the catchall conf file.) Follow the virtual host tutorial with these values:

`ServerName solarprotocol.net`
`ServerAlias www.solarprotocol.net`

### 1) Install Snap

`sudo apt install snapd`
`sudo reboot`
`sudo snap install core; sudo snap refresh core`

### 2) Install Certbot

`sudo snap install --classic certbot`
`sudo ln -s /snap/bin/certbot /usr/bin/certbot`

`sudo certbot --apache`
you will be asked to enter an email address - in the future we will create a webmaster email for all SP server
confirm terms of service
opt out of EFF emails
