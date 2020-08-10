# distributed-dynamic-IP-exchanger-API

## v1-files
Version 1 of the API uses CVS and JSON files.

### api.php
This manages GET and POST requests on the server

GET requests allow for querying PV data from the device
POST requests allow other devices on the network to update the IP list to account for dynamic IP issues

### clientPostIP.py

This script updates the IPs on the other devices on the network

### solarProtocol.py
This script queries the PV data from the other devices and determines if the local device should be point of contact and updates the DNS if so

### deviceList.json
This is where mac, ip and timestamp info from devices on the network is stored. The file needs to exist, but it can be blank... It isn't completely necessary to prepopulate it with the IP addresses, but if not you need to manually make Post request or edit the files locally to start everything up.
* name and timestamp aren't required, but may be helpful in the future for debugging

format:
[{"mac":"0","ip":"0.0.0.0","time stamp":"0","name":""},
{"mac":"1","ip":"1.1.1.1","time stamp":"0","name":""}]

Set file permissions for deviceList.json
* sudo chmod a+w deviceList.json

### Environmental Variables
The API key should be changed and stored as an environmental variable on each device
* The environmental variable value is SP_API_KEY

Setting environmental variables on the Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* Variables set in the /etc/profile file are loaded whenever a bash login shell is entered. You may need to reboot after adding the variables to this file.
* When declaring environment variables in this file you need to use the export command. Do not put a space around the =.
* Add this line to bottom of /etc/profile 
	* export SP_API_KEY=api-key

## v2-mysql
NOT FUNCTIONING
 
Version 2 of the API would potentially use a mysql data base, but this is (at least for the time being) more difficult, because all three servers need to have the same mysql setup i.e. same db, table, and column names as well as the same users with all necessary permissions. This approach possibly consumes less energy that v1.

https://pimylifeup.com/raspberry-pi-mysql/

GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';

## Testing

clientGetPV.py is just for testing purposes. solarProtocol.py handles this functionality in production version.

Sample data is included in the data/tracerData2020-08-04.csv file
* date on file needs to be updated daily for testing purposes
* place this in /home/pi/EPSolar_Tracer/data/


## TO DO:
* test PHP environmental variables
* merge with the solar website stuff...