# SSL Certificates for the Solar Protocol Network

Port forwarding for 80 -> 80 must be enable to run the installation scripts.

Port forwarding for 443-> 443 must be enabled for this to take effect (8443 -> 443 must also be enabled on some residential routers to minimize troubleshooting issues).

The basic approach is that certbot is run on 1 device. The keys are then distributed to all servers.

## Installation
This is only required on the server running 
1) `sudo apt install python3-certbot-apache`
2) `sudo apt install certbot`

## Generate Certificate
3) `python utilities/updateDNS_UnitTest.py` Step 4 will only work if the server you are working on is the PoE at the moment. Navigate to the solar-protocol/backend/core directory and run this script to force PoE (Note that this may take a minute to take effect. Also another server may 'steal' it back before step 4 is run. An alternative method is to use a redirect, such as `rewrite ^/.well-known/acme-challenge/(.*)$ http://acme.example.com/$1 redirect;` but for the time being this isn't necessary.)
4) `sudo certbot --apache`
* Enter your email address when prompted
* Enter this domain name when prompted: `www.solarprotocol.net`

5) Distribute
* Copy the contents of  /etc/letsencrypt/ 
* Copy the /etc/apache2/sites-available/000-default-le-ssl.conf file



## Renewal

To manually renew, run `sudo certbot renew --apache`. This may only be possible to run within 30 days of expiration.

Automated renewing is controlled by this file: /etc/cron.d/certbot. Do not copy this file to the other servers.
