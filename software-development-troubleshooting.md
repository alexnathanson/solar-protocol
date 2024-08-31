# Software & Network Troubleshooting

Troubleshooting the Solar Protocol network can be extremely difficult and confusing primarily because it is often unclear if a problem is caused internally in a server or because of something in the wider network.

## General

### Logs

Start script logs are located in /home/pi/solar-protocol/start.log

Backend core logs are located in the /home/pi/solar-protocol/backend/runner.log

Charge controller data collection log is located at /home/pi/solar-protocol/chargecontroller/datalogger.log

Apache and PHP errors are logged in /var/log/apache2/error.log

### Admin Console

Go to the 'network status' tab in the admin interface. Are there servers listed that are returning data?
* If a server is listed an it isn't returning data, click on the IP address.
	* If the link works, it likely indicates a problem with that server and not the server you are looking at currently
	* If the link doesn't work, it may just mean that that server is offline. Try SSHing in to it to confirm it is offline and checkback when it turns back on.

### Is it running?

This code will return a list of Python programs currently running.

`ps aux | grep .py`

You should see at least 4 lines. 2 lines from root user and 2 lines from pi.

2 lines ending in 'csv_datalogger.py' (1 from root user and 1 from pi) and 2 lines ending in 'backend' (also 1 from root user and 1 from pi)

## Charge Controller Data Collection

1) Is data being recorded?
* Go to the 'local data' tab in the admin interface. Is data being recorded properly? It is generally recorded in 2 minute intervals, though some servers may record data at a different rate. (Make sure you go to the direct IP address, not the solarprotocol.net URL in case the point of entry changes while you are working.)
* You can also check that data is being recorded by going to /home/pi/solar-protocol/charge-controller/data. You should see a csv file for every day. (Remember that the time stamp is in server local time, not your local time.)

2) Check if csv_datalogger.py is running

* SSH in to device
* run `ps aux | grep .py`
* you should see 1-2 lines ending in 'csv_datalogger.py' (1 from root user and 1 from pi)
* check the log file at /home/pi/solar-protocol/chargecontroller/datalogger.log
* confirm that the automated start up code is correct. Check with `systemctl status solar-protocol`, and look at the logs with `journalctl -u solar-protocol`

## Solar Protocol Network Troubleshooting.

Troubleshooting the Solar Protocol network can be difficult and confusing primarily because it is often unclear if a problem is caused internally in a server or because of something in the wider network.

Most troubleshooting involves checking the logs for an individual server that is either the source of the problem or is showing some indication that there is a problem somewhere on the network:

1) check the logs at 'home/pi/solar-protocol/backend/runner.log'
* jump to the bottom of the file
* scroll up a little to the beginning of the most recent run

The beginning of a run is indicated by the text
```
Loop frequency: 20 minutes
Run number 3 at 03/30/2023 00:41:00
```

The end of a run is indicated by the text

```
Completed run 2 at 03/30/2023 00:21:58
Exceptions: viz
```

The details will change based on the specific times and if there are any exceptions.

Some exceptions lead to wider problems in the next while other just indicate that something is broken but it doesn't have cascading effects. "Viz" is a very common exception to see. It indicates a problem with the visualization, but doesn't impact anything else negatively.

### Client Post IP Script

This shows whether posting to other servers in the network was successful or unsuccessful.

If you see any lines that say 'Post to IP_ADDRESS successful' it means that there isn't an issue here and that anything listed as unsuccessful indicates that remote server is either off or there is a problem.

If you don't see any successful posts (except for maybe localhost) you will probably see some indcation of a password error. Contact the network administrator to get the proper password for your server to make POST requests.

### Solar Protocol Script

At the top you will see a list of IP and underneath that you will see a list of HTTP connection errors.

The IPs listed at the top that didn't return errors, should match the successful Posts in the previous section.

If your server is the point of entry you should see a message below that includes the line `<ErrCount>0</ErrCount>`. This indicates that it was successfully able to point the DNS to itself and become the point of entry. If it is the point of entry and you get an error, it likely indicates a password issue with the DNS gateway and you should contact the network administrator.

If you are not the point of entry for that particular run, but you suspect an issue with the DNS gateway, the best thing is to search the file for the text 'Point of Entry' and see if an error occurred. 

Note that a common issue here is that a server may be the point of entry and the DNS may be pointed to it, but there is a network access issue (i.e. port forwarding restrictions, firewalls, etc) that is causing the problem. In this case, confirm that port 80 on your server is open to the public. One easy way to do this is to use a cell connection(not wifi) and try to access the direct IP address on your phone.

### Get Remote Data Script

This saves data to the 'home/pi/local/data' directory. The successfull IPs should match the successful IPs in the previous sections. You can confirm that it is storing data correctly by navigating to that directory and checking when those files were last modified with `ls -l`. The servers with successful IPs should have been modified at about the time this run occurred.

### Running Viz

TBD

### Create  HTML

TBD