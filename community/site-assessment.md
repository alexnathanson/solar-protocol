# Site Assessment
What physical infrastructure is needed to host a Solar Protocol server?

## Solar Insolation
<p>
Assessing how appropriate your location is for a solar powered server is crucial to the success of the project. This primarily involves identifying obstructions that may block sunlight during the hours of 9am-3pm.
</p>

<p>

* In some regions, there are digital tools that may help identify obsctructions based on satelite data.
	* US
		* Google Sunroof
		* PV Watts
	* Germany
		* https://www.eon.de/de/pk/solar.html
</p>

* What is your site's longitude and latitude?
* What are the potential obstructions?
	* If above 23 degress latitude north, the south side needs to be clear of obstructions
	* If below 23 degress latitude south, the north side needs to be clear of obstructions

## Physical Access

* Are you able to site the hardware in place?
* Is it a safe location?
* Can it stay in place for at least a year?
* Can you run the appropriate cables?

## Internet Connectivity

* Does your site have wifi?
* Does your site have an ethernet cable to a router?
* Static vs dynamic public IP
* Port forwarding
	* http - port 80
	* ssh - port 20	
* Minimum speed
	* 25mb/s up
	* 25mb/s down

## Time Commitment

* Installation
	* Hardware installation
		* Enclosure + Electronics
		* Battery
		* Solar module
	* Software installation
		* network details
* Commitment to trouble shooting
	* Checking system operation
* See the community agreement for a detailed breakdown of responsibilities