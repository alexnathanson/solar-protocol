# Solar Protocol - Classic (V0.1.0)

A system for load balancing and serving content based on photovoltaic logic.
=======

<strong>
This branch is an archive of the version of Solar Protocol that ran from roughly 2021 - summer 2024. It is being kept for future reference and for servers that may be running the old version. It is being depreciated and should not be installed on new devices.
</strong>
<strong>
Updates to maintain compatability can be done manually or by pulling relevent files (typically only those with frontend changes) from the main branch with the code below<br>

`git checkout solarprotocol-classic`
`git checkout main PATH_TO_FILE`
</strong>

A repository for a solar powered network of servers that host a distributed web platform. Project by Tega Brain, Alex Nathanson and Benedetta Piantella. Supported by Eyebeam Rapid Response for a Better Digital Future fellowship.

Content at <a href="http://www.solarprotocol.net">solarprotocol.net</a> is served by whichever server in our network is in the most sunlight at a given time. (We are basing this off of the solar module wattage.)

It is a decentralized network. Each server checks in with the other devices and independently determines if it should be the 'point of entry' (poe) for the system.

Server stewards have the ability to host their own content on the devices as well.

Solar Protocol is an art project exploring the poetics of internet infrastructure; as well as an education and research platform for exploring energy efficient and energy aware web design; and ecologically responsive internet protocols, among many other things.

Our work is inspired by the great work done previously by the folks at Low Tech Magazine.

## Installation

https://github.com/alexnathanson/solar-protocol/blob/master/installation.md

## API documentation

https://github.com/alexnathanson/solar-protocol/blob/master/API.md

## Hardware install notes  

[Notes in a doc here](https://docs.google.com/document/d/1hdcTf9xUmsjRPd3waJEkQf1Bjive8Z6RmyWv_p5n8Is/edit)

## Hardware Troubleshooting & Maintenance

https://github.com/alexnathanson/solar-protocol/blob/master/hardware-troubleshooting-and-maintenance.md

<!-- ### FRONT END
* Code for an energy responsive front end is in test-site folder
* To test, set up a virtual environment and install requirements.txt
 -->

## Collaborate with us!

This is a growing global collaborative project and there are many ways to contribute. Some tasks that a volunteer could take on are listed below. Please get in touch if you would like to contribute in some way.

### Software development

* Enable better network analytics
* Refactor the admin console
* Write a script to periodically run a software update automatically
* Write a script to run the backend processes based on battery status, rather than just time

### Design

* Admin console redesign
* Solar Protocol header for steward pages

### Content

* Do you have a great idea for something that could make use of this unique system? It could be an art project, research project, essay, etc.

### Other

* Can you conduct an LCA of the hardware we use?
* Can you help identify an accurate way to quantify the energy consumed by transferring data across the internet?
