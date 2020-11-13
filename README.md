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
* make an installer.sh (not time sensitive)
* add link to documention somewhere (https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip)
* make a script for pull updates from the git repo that automates resetting permissions as needed (not time sensitive)
	* create a system for updating devices remoting (maybe every evening at midnight?)
	* make 2 branches - 1 live version and 1 development version

### FRONTEND

* Basic energy data collection for different sized pages and traffic. (not time sensitive)
* add poc log to front-end page
* network visualizations
* how do we add content from hosts?
	* make our own personal sites for the servers

### BACKEND

* make sure the point of contact log starts rewriting data after 100 entries and doesn't keep adding data forever
* develop API for security best practices - API keys, environmental variables, etc.
* refactor admin console (not time sensitive)
* add password/ login requirements to admin console
* system for adding/ removing network nodes

### CONTENT

* Documentation of our work
* Public programming around this
	* Slow/low video streaming + audio?
* Personalization from hosts
	* Eg. Aesthetic personalization such as name, banner, welcome note. And an html page, which could include a pdf.
* Directory of solar powered sites
