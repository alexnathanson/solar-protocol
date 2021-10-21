# DNS Gateway

The contents of this directory run on a server redirected through dns.solarprotocol.net (redirection through dns.solarprotocol.net isn't working currently so we are temporarily using https://server.solarpowerforartists.com)

This handles requests from servers on the network to repoint the DNS and manages the access lists.

This server also handles some functionality that we were previously using 3rd parties for, such as retrieving our public IP.

In the future, this function could be added to the internal solar protocol API and be kept "in network"


## API
url https://server.solarpowerforartists.com/ 

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

test
`https://server.solarpowerforartists.com/?test=AN-IP-ADDRESS` updates the DNS
