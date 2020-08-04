# distributed-dynamic-IP-exchanger-API

## mysql

All three servers need to have the same mysql setup i.e. same db, table, and column names as well as the same users with all necessary permissions.

https://pimylifeup.com/raspberry-pi-mysql/

GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';

## Testing
Remember to update data file date for testing purposes...

clientGetPV.py is just for testing purposes. solarProtocol.py handles this functionality in production version.

## TO DO:
* fix api post for IP list json
* have clientPostIP.py access IP list and post to those IPs
* solarProtocol needs to access IP list and get PV data from those IPs
* merge with the solar website stuff...