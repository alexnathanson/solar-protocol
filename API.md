# Solar Protocol API

An API for updating dynamic IPs and comparing data between distributed Raspberry Pis.

## API V1 v1-files
Version 1 of the API reads and writes CVS and JSON files.

### api.php
This manages GET and POST requests on the server

* GET requests allow for querying PV data from the device
* POST requests allow other devices on the network to update the IP list to account for dynamic IP issues

### clientPostIP.py

This script updates the IPs on the other devices on the network

* this should be set on a cron timer

### solarProtocol.py
This script queries the PV data from the other devices and determines if the local device should be point of contact and updates the DNS if so

* this should be set on a cron timer
* update the subCall to the appropriate DNS updater system being used

### deviceList.json
This is where mac, ip, timestamp, and device name info from devices on the network is stored. The file needs to exist, but it can be blank... It isn't completely necessary to prepopulate it with the IP addresses, but if not you will need to manually make Post requests or edit the files locally to start everything up.
* name and timestamp aren't required, but may be helpful in the future for debugging

format:
[{"mac":"0","ip":"0.0.0.0","time stamp":"0","name":""},
{"mac":"1","ip":"1.1.1.1","time stamp":"0","name":""}]

Set file permissions for deviceList.json
* sudo chmod a+w deviceList.json

### API Key
The API key should be added to the local.json file

<!--
The API key should be changed and stored as an environmental variable on each device
* The environmental variable key is SP_API_KEY

Setting environmental variables on the Pi (source https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)
* Variables set in the /etc/profile file are loaded whenever a bash login shell is entered. You may need to reboot after adding the variables to this file.
* When declaring environment variables in this file you need to use the export command. Do not put a space around the =.
* Add this line to bottom of /etc/profile (replace this temp key with a new one)
	* export SP_API_KEY=tPmAT5Ab3j7F9
-->

## v2-mysql
NOT FUNCTIONING
 
Version 2 of the API would potentially use a mysql data base, but this is (at least for the time being) more difficult, because all three servers need to have the same mysql setup i.e. same db, table, and column names as well as the same users with all necessary permissions. This approach possibly consumes less energy that v1.

https://pimylifeup.com/raspberry-pi-mysql/

GRANT ALL PRIVILEGES ON exampledb.* TO 'exampleuser'@'localhost';

## API Syntax

### GET
clientGetPV.py is just for testing purposes. solarProtocol.py handles get request when they system is operational. You can also use a browser to make a get request.

Possible keys for get requests

* value - returns the specified value from the most recently collected line of data
	* Example: http:// + URL + /api/v1/api.php?value=PV-voltage
	* Possible values (replace spaces with "-"):
		* PV current
		* PV power H
		* PV power L
		* PV voltage,
		* battery percentage
		* battery voltage
		* charge current
		* charge power H
		* charge power L
		* load current
		* load power
		* load voltage
		* datetime
* line - returns the specified line from the current data logger file with headers in JSON format
	* Example: http:// + URL + /api/v1/api.php?line=0
	* Possible values:
		* len - returns the number of rows in the file
		* head - returns the column headers
		* 0 - returns the most recently collected line of data
		* increment up to move back in time from 0 to retrieve any other row. For example, 1 will return the 2nd most recent row.
* file - returns a specific file
	* Example: http:// + URL + /api/v1/api.php?file=deviceList
	* Possible values:
		* deviceList - returns the deviceList.json file contents (should be changed to a POST not a GET)
		* 0 - returns present day data 
		* 1 - returns present day + previous day
		* 2 - returns present day + previous 2 days
		* 3 - returns present day + previous 3 days
		* 4 - returns present day + previous 4 days
		* 5 - returns present day + previous 5 days
		* 6 - returns present day + previous 6 days
		* list - returns list of all CC files
		* [file name]

<p>
Browser Example: http://solarprotocol.net/api/v1/api.php?value=PV-voltage would return the most recent PV voltage
</p>

### POST

Possible keys for Post requests:
* apiKey
* stamp - time stamp
* ip
* mac
* name - name of device
* log - log of "point of contact" events

Python Example: 

import requests


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName
x = requests.post('http://www.mywebsite.xyz/api/v1/api.php', headers=headers,data = myString)
