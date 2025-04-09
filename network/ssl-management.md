# SSL Certificates for the Solar Protocol Network

Port forwarding for 80 -> 80 and 443 -> 443 must be enable. (8443 -> 443 must also be enabled on some residential routers to minimize troubleshooting issues).

The basic approach is that certbot generates and renews the certificates on only 1 device. The key certificate and private key is then distributed to all servers on the network.

## 1) Installation
This is required for all servers:<br>
1.1) `sudo apt install python3-certbot-apache`<br>
1.2) `sudo apt install certbot`<br>
1.3) `a2enmod ssl`

## 2) Generate Certificate

Step 2 is only required for the generating server and should NOT be done on all servers.<br>

2.1) Set PoE

`cd /home/pi/solar-protocol/backend/core`<br>
`python utilities/updateDNS_UnitTest.py`

The next step will only work if the server you are working on is the PoE at the moment. Navigate to the solar-protocol/backend/core directory and run this script to force PoE (Note that this may take a minute to take effect. Also another server may 'steal' it back before step 4 is run. An alternative method is to use a redirect, such as `rewrite ^/.well-known/acme-challenge/(.*)$ http://acme.example.com/$1 redirect;` but for the time being this isn't necessary.)

2.2) Run Certbot

`sudo certbot --apache`
* Enter your email address when prompted
* Enter this domain name when prompted: `solarprotocol.net www.solarprotocol.net`

## 3) Manually distribute to the servers in the network

3.1) Retrieve files<br>
* Copy the /etc/letsencrypt directory (this is necessary because the permissions don't let you directly scp the files we need.)
	* `sudo chmod 755 /etc/letsencrypt` temporarily change the permissions of this directory (may need to do this recursively)
	* `sudo cp -r /etc/letsencrypt /home/letsencrypt`
	* `sudo chmod 700 /etc/letsencrypt` revert permissions 
* Change owner of this new directory to pi `sudo chown -R pi:pi /home/letsencrypt`
* From your machine, retrieve the directory with pscp. (This works on windows. The syntax may need to change for other operating systems.)
	* `pscp -r -i "path\of\the\privatekey\letsencrypt" -P 22 pi@DST_IP:/home/letsencrypt C:\path\of\source\directory\solar-protocol\network\letsencrypt` (letsencrypt directory is ignored in git) 
* `sudo rm -r /home/letsencrypt ` delete the temporary copy on the server

3.2) Distribute files to all servers<br>
* create a temp directory for these files on the destination server: `sudo mkdir /home/pi/temp-ssl`
* set permissions and ownship of directory pi if not already: `sudo chown -R pi:pi /home/pi/temp-ssl` (If errors still occur change permissions to chmod 755. If you get an error about the group, just change the own to pi instead of pi:pi)
* SCP the directory you copied from your machine to the target server. The only necessary files are the ssl certificate, private key, and configuration files (but it's usually easier to just copy the entire directory). Note that if the server is already using th defaul ssl conf name, you may need to change the file names.
	* `pscp -r -i "path\of\the\privatekey\letsencrypt" -P 22 "C:\path\of\source\directory\...\letsencrypt" pi@DST_IP:/home/pi/temp-ssl`
* Copy the contents of /etc/letsencrypt/live/solarprotocol.net (these are the private keys and certificates)
	* `sudo cp -R /home/pi/temp-ssl/letsencrypt/live/solarprotocol.net /etc/letsencrypt/live/solarprotocol.net`
	* If you need to confirm this worked, change permissions of live directory `sudo chmod 755 /etc/letsencrypt`
	* Once confirmed, revert the permissions changes back to "drwx------ 4 root root" with `sudo chmod 700 /etc/letsencrypt` (untested)
* Copy the Apache SSL config file (This is only required the first time you distribute it, not for renewals.):
	* `sudo cp /home/pi/solar-protocol/network/000-default-le-ssl.conf /etc/apache2/sites-available/000-default-le-ssl.conf`
* Copy the renewal/solarprotocol.net file to the /etc/letsencrypt/renewal/ directory (only required when first installing, not for renewals0
* enable the sites with `sudo a2ensite 000-default-le-ssl.conf` or if that doesn't work you can create a new symlink with `sudo ln -s ../sites-available/000-default-le-ssl.conf` (this probably shouldn't be necessary for renewals, just when first installing)
* restart apache `sudo systemctl restart apache2`

## 4) Renewal
Renewal can only happen within 30 days of expiration.

To manually renew, run:<br>
4.1) navigate to the solar-protocol/backend/core directory and run `python utilities/updateDNS_UnitTest.py`<br>
4.2) `sudo certbot renew --apache` <br>
4.3) Distribute the new files
<p>
Automated renewing is controlled by this file: /etc/cron.d/certbot. Do not copy this file to the other servers. It is expected that this will fail, because the server will not necessarily be the PoE at the moment its run. In the future changing this script to run the updateDNS script first will increase the likelihood of success.
</p>

Autodistribution could also potentially be possible with rsync.

To get auto renew working:<br>
* check if it is time to renew
* enable PoE
* run renewal
* distribute keys

## Troubleshooting

* Run `sudo certbot certificates` to view active certificates with expiration dates
* Remember that SSL certificates are tied to URLs not IPs, so testing that it works with either your local or public IP will fail.
