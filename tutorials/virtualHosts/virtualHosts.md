# Adding Virtual Hosts and Subdomains to your Apache server

The purpose of this is to redirect another url, like www.mygreatproject.com for example, to the proper directory within the server.

It is recommended to follow the below instructions to use different conf files for each redirect, but an example for a single conf file with multiple named configurations is included too. More info about choosing multiple files or just 1 is at http://joabj.com/Writing/Tech/Tuts/Apache/Apache-Subdomains.html

## Setup

* Create your content and place it the directory you plan to use. For example, `home/pi/local/www/mygreatproject`
* Set read permissions for that directory `sudo chmod -R 755 /home/pi/local/www/mygreatproject/`
* Update the DNS registry accordingly. Note that this is not dynamic so if your public IP changes your connection will be severed, unless you implement a dynamic IP updater.

## Steps

### Step 1

Copy the default file. The name of the file doesn't really matter, but the convention is that it has the same name as the URL. It must end in .conf

`sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/mygreatproject.com.conf`

### Step 2

Edit the file. 

`sudo nano mygreatproject.sun.conf`

Underneath the ServerAdmin line, add the following line (obviously replace mygreatproject.com with your URL)
`ServerName mygreatproject.com`

If you have any server aliases add them on the next line. If you are not using an alias, then ignore this. `ServerAlias www.mygreatproject.com`

Change the document root path to the location of your site root directory
`DocumentRoot /home/pi/local/www/`

### Step 3

Enable the subdomain or domain

`sudo a2ensite mygreatproject.com.conf`

then restart Apache

`sudo service apache2 restart` or `sudo systemctl reload apache2`

## Troubleshooting

The default config file is whichever one is loaded first, which is why the default is named 000-default.conf

### Access denied

If you attempt to go to the URL in a browser and get a response that says access denied, add these lines to either the virtual host conf file or the global apache conf file (/etc/apache2/apache2.conf). 

(the path should be your document root).

`<Directory /home/pi/local/www>`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
`</Directory>`

If you are adding them to apache2.conf, its best to place it near the other directory config blocks. If you are adding them to the virtual host conf file it goes within the `<VirtualHost></VirtualHost>` section for your server name. 

### No connection

This could be an issue with the DNS registry.

### No connection to the main SP site

This hasn't been tested on a server acting as the Solar Protocol PoE. If enabling this makes solarprotocol.net inaccessible, some work around having a catch all virtual server will be necessary.

### including .htaccess files

If you need to use an .htaccess file in the directoy add `AllowOverride All` to the apache2.conf entry for the directory the you created for the virtual host.

`<Directory /home/pi/local/www>`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`AllowOverride All`<br>
`</Directory>`