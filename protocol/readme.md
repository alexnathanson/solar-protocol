# solar protocol - protocol

## Runner

The runner controls when the other scripts are run based on battery status

* >90% every 10 minutes
* >70% & <= 90% every 15 minutes
* >50% & <=70% every 20 minutes
* <=50% every 30 minutes

## Core

These scripts are the client side processes that interact with the API. They enable devices to pass data around the network. These scripts are run via run.py

* clientPostIP.py posts local data to the other devices on the network (the calls are managed by the PHP scripts in frontend/api/)
* solarProtocol.py checks if the local server is the 'point of entry' (poe) for the system and updates the DNS if it is
* SolarProtocolClass.py provides some common functionality. In the future this can be expanded to store state now that everything is run centrally.

## Create HTML

These scripts are run via run.py

The templates directory contains template files for all of the pages

* html.py is a static site generator. It updates the page templates (saves them in the frontend directory)
* viz.py produces the data visualization of the network featured on the home page

## Data

* devices.json stores data received from other devices 

## Protect

* these scripts are the login pages for the admin console on the site

