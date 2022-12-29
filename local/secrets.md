## secrets.json

Used for passwords and keys

### network key

Allows announcing your server to the other ones in the network

Talk to an administrator for this key, then set it with `solar-protocol set-network-key NETWORK-KEY-GOES-HERE`

### app id

Needed for getting local weather data from openweathermap.org. Ask an administrator for it, then set with `solar-protocol set-app-id APP-ID-GOES-HERE`

### dns key

To become the active server, this key is sent to our DNS gateway. If the gateway has your key in the allowlist, it will update beta.solarprotocol.net to your current server's IP.

NEVER SHARE THIS KEY - use `solar-protocol get-dns-hash` and share that with an admin instead

---

### dnspassword

The `dnspassword` is used to update the DNS records for the solar protocol network. It should be left blank - only the DNS gateway uses this.

## admin.htpasswd

Used to protect your server's local settings.

To add or change your admin settings page password, run `solar-protocol set-admin-password USERNAME_HERE PASSWORD_HERE`.
