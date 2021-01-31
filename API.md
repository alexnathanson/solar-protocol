# Solar Protocol API V1

An API for communicating between distributed Raspberry Pis and making system data accessible
* Network communication between servers on the network is done with POST requests via the api.php end point 
* Retrieving data from charge controllers is done with GET requests via the chargecontroller.php end point.

## api.php
This manages POST requests on the server

* POST requests allow other devices on the network to update the IP list to account for dynamic IP issues

### clientPostIP.py

This script updates the IPs on the other devices on the network

* this should be set on a cron timer

### solarProtocol.py
This script queries the PV data from the other devices and determines if the local device should be point of entry and updates the DNS if so

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


### POST

Possible keys for post requests:
* apiKey
* stamp - time stamp
* ip
* mac
* name - name of device
* log - log of "point of entry" events

Python Example: 
```
import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

myString = "api_key="+apiKey+"&stamp="+str(time.time())+"&ip="+myIP+"&mac="+myMAC+"&name="+myName
x = requests.post('http://www.mywebsite.xyz/api/v1/api.php', headers=headers,data = myString)
```

## chargecontroller.php
This manages open access GET requests for local charge controller data

* GET requests allow for querying PV data from the device

### Syntax

clientGetPV.py is just for testing purposes. solarProtocol.py handles get request when they system is operational. You can also use a browser to make a get request.

Possible keys for get requests

* value - returns the specified value from the most recently collected line of data
	* Example: http://solarprotocol.net/api/v1/chargecontroller.php?value=PV-voltage
	* Possible values:
		* PV-current
		* PV-power-H
		* PV-power-L
		* PV-voltage
		* battery-percentage
		* battery-voltage
		* charge-current
		* charge-power-H
		* charge-power-L
		* load-current
		* load-power
		* load-voltage
		* datetime
	* Modifier: duration - returns the specified value over a given number of days, up to 7.
		* Example: http://solarprotocol.net/api/v1/chargecontroller.php?value=PV-voltage&&duration=1
		* Possible values:
			* [integer] - specifies the number of days starting at 1
* line - returns the specified line from the current data logger file with headers in JSON format
	* Example: http:// + URL + /api/v1/chaergecontroller.php?line=0
	* Possible values:
		* len - returns the number of rows in the file
		* head - returns the column headers
		* 0 - returns the most recently collected line of data
		* increment up to move back in time from 0 to retrieve any other row. For example, 1 will return the 2nd most recent row.
* day - returns all the data for a given day
	* Example: http://solarprotocol.net/api/v1/chargecontroller.php?day=len
	* Possible values:
		* 1 - returns most recent day of data (typically the present day)
		* 2 - returns the 2 most recent days
		* 3 - returns the 3 most recent days
		* 4 - returns the 4 most recent days
		* 5 - returns the 5 most recent days
		* 6 - returns the 6 most recent days
		* 7 - returns the 7 most recent days
		* list - returns list of all available files. Each file represents 1 day's worth of data.
		* len - returns the amount of files available. Each file represents 1 day's worth of data.
		* [file name without file suffix] - example: http://solarprotocol.net/api/v1/chargecontroller.php?day=tracerData2020-05-17
* systemInfo - provides information about the system
	* Example: http://solarprotocol.net/api/v1/chargecontroller.php?sysInfo=tz
	* Possible values:
		* tz - returns the timezone for the server
<p>
Browser Example: http://solarprotocol.net/api/v1/chargecontroller.php?value=PV-voltage would return the most recent PV voltage
</p>
<p>
Python and JS examples available in utilities directory
</p>