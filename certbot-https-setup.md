# Installation for Certbot

none of this works...

## links

https://certbot.eff.org/instructions?ws=apache&os=ubuntufocal

https://peppe8o.com/use-lets-encrypt-and-certbot-to-secure-raspberry-pi-hosted-websites-automatically/


## Instructions

### Pre-Setup

#### update and upgrade

`sudo apt update && sudo apt upgrade`

#### create sp virtual host
In order for the automated process to work, we need to explicitly create a virtual host file. (The default is that we direct the catchall conf file.) Follow the virtual host tutorial with these values:

`ServerName solarprotocol.net`
`ServerAlias www.solarprotocol.net`

#### install ssl module
* Install ssl module

`sudo a2enmod ssl`

* restart apache

`sudo systemctl restart apache2`

### 1) Install Snap

`sudo apt install snapd`
`sudo reboot`
`sudo snap install core; sudo snap refresh core`

### 2) Install Certbot

`sudo snap install --classic certbot`
`sudo ln -s /snap/bin/certbot /usr/bin/certbot`

try:
`sudo certbot --apache -v`
you will be asked to enter an email address - in the future we will create a webmaster email for all SP server
confirm terms of service
opt out of EFF emails

else run only the creation of the cert

`sudo certbot certonly --apache -v`

### 3) Configure Apache


## Troubleshooting

test apache configs `apachectl configtest`




`SSLEngine on`
`SSLCertificateFile /etc/letsencrypt/live/solarprotocol.net/fullchain.pem`
`SSLCertificateKeyFile /etc/letsencrypt/live/solarprotocol.net/privkey.pem`
`Include /etc/letsencrypt/options-ssl-apache.conf`


Misc:
is this needed?
`a2enmod http2`




######


https://github.com/acmesh-official/acme.sh


1) install

`curl https://get.acme.sh | sh -s email=my@example.com`

2) close and reopen/reboot

close and reopen the ssh connection to enable (if that doesn't work restart)

`sudo reboot`

3) issue a cert for multiple domains

`acme.sh --issue -d www.solarprotocol.net -d www.solarprotocol.net -w /home/pi/solar-protocol/frontend`

do this for each site root directory

`acme.sh --issue -d example.solarprotocol.net -d www.solarprotocol.net -w /home/pi/local/www`


4) install cert

`sudo acme.sh --install-cert -d solarprotocol.net --cert-file /home/pi/.acme.sh/solarprotocol.net/solarprotocol.net.cer --key-file /home/pi/.acme.sh/solarprotocol.net/solarprotocol.net.key --fullchain-file /home/pi/.acme.sh/solarprotocol.net/fullchain.cer --reloadcmd     "service apache2 force-reload"`



might be a permissions issue???