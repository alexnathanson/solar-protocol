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

### networkkey

This key is used to join the network - it is sent when announcing your server to other servers. Talk to an administrator for the needed key.

### appid

The `appid` is used to get local weather data from openweathermap.org. Talk to an administrator for the needed id.

### dnskey

To become the active server, this key is sent to our DNS gateway. If the gateway has your key in the allowlist, it will update beta.solarprotocol.net to your current server's IP.

This key can be generated with `solar-protocol generate-key`, or via the admin page. Send this key to an administrator to participate in the network.

### dnspassword

The `dnspassword` is used to update the DNS records for the solar protocol network. It should be left blank - only the DNS gateway uses this.

## admin.htpasswd

Used to protect your server's local settings.

To add or change your admin settings page password, run `solar-protocol set-admin-password USERNAME_HERE PASSWORD_HERE`.
