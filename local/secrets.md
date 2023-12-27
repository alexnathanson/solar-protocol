## secrets.json

Used for passwords and keys

### network key

Allows announcing your server to the other ones in the network

Ask an administrator for this key, then update `{"networkkey": "KEY_GOES_HERE"}`.

### app id

Needed for getting local weather data from openweathermap.org.

Ask an administrator for this key, then update `{"appid": "KEY_GOES_HERE"}`.

### dns key

NEVER SHARE THIS KEY 

To become the active server, this key is sent to our DNS gateway.
If the gateway has your key in the allowlist, it will update beta.solarprotocol.net to your current server's IP.

Use `solar get-dns-hash` and share that with an admin instead

---

### dnspassword

The `dnspassword` is used to update the DNS records for the solar protocol network. It should be left blank - only the DNS gateway uses this.

---

## admin.htpasswd

Used to protect your server's local settings.

To add or change your admin settings page password, look at the `set-admin-credentials` function in the `solar` script.
