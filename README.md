# distributed-dynamic-IP-exchanger-API

## v1-files

Set file permissions for deviceList.json
* sudo chmod a+w deviceList.json
## v2-mysql

Version 2 of the API would potentially use a mysql data base, but this is (at least for the time being) more difficult, because all three servers need to have the same mysql setup i.e. same db, table, and column names as well as the same users with all necessary permissions. This approach possibly consumes less energy that v1.

https://pimylifeup.com/raspberry-pi-mysql/

GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';

### deviceList.json
format:
[{"mac":"0","ip":"0.0.0.0","time stamp":"0"},
{"mac":"1","ip":"1.1.1.1","time stamp":"0"}]

## Testing
Remember to update data file date for testing purposes...

clientGetPV.py is just for testing purposes. solarProtocol.py handles this functionality in production version.

Sample data is included in the tracerData2020-08-04.csv file


## TO DO:
* fix api post for IP list json
* have clientPostIP.py access IP list and post to those IPs
* solarProtocol needs to access IP list and get PV data from those IPs
* merge with the solar website stuff...