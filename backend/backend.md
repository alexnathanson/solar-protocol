# Backend

The contents of this directory all run on each of the servers.

## API

* clientPostIP.py posts local data to the other devices on the network (the calls are managed by the PHP scripts in frontend/api/)
	* this is run via chron
* deviceList.json stores data received from other devices 
* solarProtocol.py checks if the local server is the 'point of entry' (poe) for the system and updates the DNS if it is
	* this is run via chron
* SolarProtocolClass.py provides some common functionality

## Create HTML

* the templates directory contains template files for all of the pages
* create_html.py is a static site generator. It updates the page templates (saves them in the frontend directly) and runs the viz.py script
	* this is run via chron
* viz.py produces the data visualization of the network featured on the home page

## Protect

* these scripts are the login pages for the admin console on the site

## Visualization

## get_env & set_env

* these scripts enable setting and getting passwords