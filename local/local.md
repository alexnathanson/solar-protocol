# Local Directory

This directory contains settings that are unique to each server

## local.json

Used for non-standard installs

### httpPort [number]

if you need to change the port you are serving from

### interface [wlan0 | eth0]

How the server connects to the internet. Defaults to `wlan0` but change to `eth0` if you are wired in.

## secrets.json

Used for passwords and keys

### apikey

This key gives access to update local files, like your server name in local.json, or your server image in serverprofile.gif.

You should never share this key. Generate a new key by running `solar-protocol generate-key`.

### dnskey

This key is used to join the network - it is added to the solar protocol dns server, and used when your server wants to become the active one. 

This key can be generated with `solar-protocol generate-key`.

### dnspassword

The `dnspassword` is used to update the DNS records for the solar protocol network. It should be left blank - only the DNS gateway uses this.

### appid

The `appid` is used to get local weather data from openweathermap.org. Talk to an administrator for the needed id.

## admin.htpasswd

Used to protect the admin settings page for your server. THIS FILE SHOULD NEVER BE EDITED BY HAND. Use the settings page or commandline.

To add or change your admin settings page password, run `solar-protocol set-admin-password USERNAME_HERE PASSWORD_HERE`.
