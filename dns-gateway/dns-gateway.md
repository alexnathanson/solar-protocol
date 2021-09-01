# Traffic controller

The contents of this directory run on a server redirected through dns.solarprotocol.net

This handles requests to repoint the DNS and manages the white/black lists. In the future it will also be able to provide the lists to clients as needed.

This server also handles some functionality that we were previously using 3rd parties for, such as retrieving our public IP. In the future, this function could be added to the internal solar protocol API and be kept "in network"


## API
url https://server.solarpowerforartists.com/ (redirection through dns.solarprotocol.net isn't working currently)

### GET requests

ip & key updates the DNS record<br>
`https://server.solarpowerforartists.com/?ip=0.0.0.0&key=123456789`

list returns the hash access list<br>
`https://server.solarpowerforartists.com/?list=true` returns white list<br>
`https://server.solarpowerforartists.com/?list=false` returns black list

myip returns the client's public IP address<br>
`https://server.solarpowerforartists.com/?myip`

<!-- ### POST requests
none currently -->