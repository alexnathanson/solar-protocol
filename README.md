# distributed-dynamic-IP-exchanger-API

## v1-files


## v2-mysql

Version 2 of the API would potentially use a mysql data base, but this is (at least for the time being) more difficult, because all three servers need to have the same mysql setup i.e. same db, table, and column names as well as the same users with all necessary permissions. This approach possibly consumes less energy that v1.

https://pimylifeup.com/raspberry-pi-mysql/

GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';

## Testing
Remember to update data file date for testing purposes...

clientGetPV.py is just for testing purposes. solarProtocol.py handles this functionality in production version.

Sample data is included in the tracerData2020-08-04.csv file


## TO DO:
* fix api post for IP list json
* have clientPostIP.py access IP list and post to those IPs
* solarProtocol needs to access IP list and get PV data from those IPs
* merge with the solar website stuff...