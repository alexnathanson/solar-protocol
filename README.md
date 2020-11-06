# Solar Protocol

A system for load balancing and serving content based on photovoltaic logic.
=======
A repository in development for a solar powered network of servers that host a distributed web platform. Project by Tega Brain, Alex Nathanson and Benedetta Piantella. Supported by Eyebeam Rapid Response for a Better Digital Future fellowship.

## Installation

https://github.com/alexnathanson/solar-protocol/blob/master/installation.md

## API documentation

https://github.com/alexnathanson/solar-protocol/blob/master/API.md

## Hardware Troubleshooting & Maintenance

https://github.com/alexnathanson/solar-protocol/blob/master/troubleshooting-and-maintenance.md


### FRONT END
* Code for an energy responsive front end is in test-site folder
* To test, set up a virtual environment and install requirements.txt

## TO DO

### General
* make an installer.sh
* X move python templater to server  - what is this?
* check any limits on the DNS api
* make sure the point of contact log starts rewriting data after 100 entries and doesn't keep adding data forever
* make a script for pull updates from the git repo that automates resetting permissions as needed
* create a system for updating devices remoting (maybe every evening at midnight?)

### FRONT END TO DO
* X Set up with real solar data from index.php
* Basic energy data collection for different sized pages and traffic. 
* Energy impact of regenerating page. What's the frequency of this?
* X move python script to backend
* add server name to device log file and fix index.html to display name.
* update data on low-res version
* add poc log to front-end page

## BACKEND TO DO

* develop API for security best practices - API keys, environmental variables, etc.
* refactor admin console
* add password/ login requirements to admin console
* system for adding/ removing network nodes


