# Adding Virtual Hosts and Subdomains to your Apache server

The purpose of this is to redirect another url, like www.mygreatproject.com for example, to the proper directory within the server.

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

If you attempt to go to the URL in a browser and get a response that says access denied add these lines to the bottom of the /etc/apache2/apache2.conf file (the path should be your document root).

`<Directory /home/pi/local/www>`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`Require all granted`<br>
`</Directory>`

If you are still running into the access denied error, you can try changing the user that owns the directory you are serving the site from. I haven't found this to solve anything, but some instructions for this process have included this step.

See instructions for this at https://ostechnix.com/configure-apache-virtual-hosts-ubuntu-part-1/

### No connection

This could be an issue with the DNS registry.