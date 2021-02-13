# Solar Protocol

A system for load balancing and serving content based on photovoltaic logic.
=======
A repository in development for a solar powered network of servers that host a distributed web platform. Project by Tega Brain, Alex Nathanson and Benedetta Piantella. Supported by Eyebeam Rapid Response for a Better Digital Future fellowship.

## Installation

https://github.com/alexnathanson/solar-protocol/blob/master/installation.md

## API documentation

https://github.com/alexnathanson/solar-protocol/blob/master/API.md

## Hardware install notes  

[Notes in a doc here](https://docs.google.com/document/d/1JErF9BTZ0PJqTYizKsbufNywM0OAiGEPdE7eItEyTxQ/edit?usp=sharing)

## Hardware Troubleshooting & Maintenance

https://github.com/alexnathanson/solar-protocol/blob/master/troubleshooting-and-maintenance.md


### FRONT END
* Code for an energy responsive front end is in test-site folder
* To test, set up a virtual environment and install requirements.txt

## TO DO

### General
* make an installer.sh (not time sensitive)
* add link to documention somewhere (https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip)


### FRONTEND

* Basic energy data collection for different sized pages and traffic. (not time sensitive)
* add poe log to front-end page
* network visualizations
* how do we add content from hosts?
	* make our own personal sites for the servers

### BACKEND

* make sure the point of entry log starts rewriting data after 100 entries and doesn't keep adding data forever
* refactor admin console (not time sensitive)
* system for adding/ removing network nodes
* filter out duplicate IP addressses on admin console
* API for plaintext redirect... ex. solarprotocol.net/idm would redirect to the IDM solar server even if its not the point of entry at that moment - another option would be to pass the IDM local content to whichever server is the point of entry as needed through the API
* Add interface in admin console to change local content

### CONTENT

* Documentation of our work
* Public programming around this
	* Slow/low video streaming + audio?
* Personalization from hosts
	* Eg. Aesthetic personalization such as name, banner, welcome note. And an html page, which could include a pdf.
* Directory of solar powered sites
