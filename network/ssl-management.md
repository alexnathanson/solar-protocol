# SSL Certificates for the Solar Protocol Network

Port forwarding for 80 -> 80 and 443 -> 443 must be enable. (8443 -> 443 must also be enabled on some residential routers to minimize troubleshooting issues).

The basic approach is that certbot generates and renews the certificates on only 1 device. The key certificate and private key is then distributed to all servers on the network.

## Installation
This is required for all servers:
1) `sudo apt install python3-certbot-apache`
2) `sudo apt install certbot`

## Generate Certificate

This is only required for the generating server and should NOT be done on all servers.

3) `python utilities/updateDNS_UnitTest.py` Step 4 will only work if the server you are working on is the PoE at the moment. Navigate to the solar-protocol/backend/core directory and run this script to force PoE (Note that this may take a minute to take effect. Also another server may 'steal' it back before step 4 is run. An alternative method is to use a redirect, such as `rewrite ^/.well-known/acme-challenge/(.*)$ http://acme.example.com/$1 redirect;` but for the time being this isn't necessary.)
4) `sudo certbot --apache`
* Enter your email address when prompted
* Enter this domain name when prompted: `www.solarprotocol.net`

5) Distribute to the servers in the network

5A) Retrieve files
* Copy the /etc/letsencrypt directory
	* `sudo chmod 755 /etc/letsencrypt` temporarily change the permissions of this directory (may need to do this recursively)
	* `sudo cp /etc/letsencrypt /home/letsencrypt`
	* `sudo chmod 700 /etc/letsencrypt` revert permissions 
* Change owner of this new directory to pi `sudo chown -R pi:pi /home/letsencrypt`
* From your machine, retrieve the directory with pscp
	* `pscp -r -i "path\of\the\privatekey\letsencrypt" -P 22 pi@DST_IP:/home/letsencrypt C:\path\of\source\directory\solar-protocol\network\letsencrypt` (letsencrypt directory is ignored in git) 
* `sudo rm -r /home/letsencrypt ` delete the temporary copy on the server

5B) Distribute files to all servers (untested!)

Copy the ssl certificate, private key, and configuration files. Note that if the server is already using th defaul ssl conf name, you may need to change the file names.

* Copy the contents of /etc/letsencrypt/live/www.solarprotocol.net
	* `sudo cp -R DIRECTORY_LOCATION/ /etc/letsencrypt/live`
	* If you need to confirm this worked, change permissions of live directory `sudo chmod 755 /etc/letsencrypt`
	* Once confirmed, revert the permissions changes back to "drwx------ 4 root root" with `sudo chmod 700 /etc/letsencrypt` (untested)
* Copy the Apache SSL config file:
	* `sudo cp /home/pi/solar-protocol/network/000-default-le-ssl.conf /etc/apache2/sites-available/000-default-le-ssl.conf`
	* restart apache `sudo systemctl restart apache2`
* Copy the renewal/www.solarprotocol.net file to the /etc/letsencrypt/renewal/ directory

Troubleshoot

## Renewal
Renewal can only happen within 30 days of expiration.

To manually renew, run:
1) `python utilities/updateDNS_UnitTest.py`
2) `sudo certbot renew --apache` 
3) Distribute the new files

Automated renewing is controlled by this file: /etc/cron.d/certbot. Do not copy this file to the other servers. It is expected that this will fail, because the server will not necessarily be the PoE at the moment its run. In the future changing this script to run the updateDNS script first will increase the likelihood of success.

Autodistribution could also potentially be possible with rsync.

## Troubleshooting

* Run `sudo certbot certificates` to view active certificates with expiration dates
* Remember that SSL certificates are tied to URLs not IPs, so testing that it works with either your local or public IP will fail.