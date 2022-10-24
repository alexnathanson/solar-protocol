# Solar Protocol

A system for load balancing and serving content based on photovoltaic logic.

=======

A repository in development for a solar powered network of servers that host a distributed web platform. Project by Tega Brain, Alex Nathanson and Benedetta Piantella. Supported by Eyebeam Rapid Response for a Better Digital Future fellowship.

Content at <a href="http://www.solarprotocol.net">solarprotocol.net</a> is served by whichever server in our network is in the most sunlight at a given time. (We are basing this off of the solar module wattage.)

It is a decentralized network. Each server checks in with the other devices and independently determines if it should be the 'point of entry' (poe) for the system.

Server stewards have the ability to host their own content on the devices as well.

Solar Protocol is an art project exploring the poetics of internet infrastructure; as well as an education and research platform for exploring energy efficient and energy aware web design; and ecologically responsive internet protocols, among many other things.

Our work is inspired by the great work done previously by the folks at Low Tech Magazine.

## Documentation

We have documented as much as possible for anyone to build upon this project.

For information about the protocol

* [api specification](docs/api.md)

If you'd like to build your own server, follow these

* [hardware buildout](https://docs.google.com/document/d/1hdcTf9xUmsjRPd3waJEkQf1Bjive8Z6RmyWv_p5n8Is/edit)
* [software installation doc](docs/installation.md)
* [hardware troubleshooting & maintenance](docs/hardware-troubleshooting-and-maintenance.md)

To develop and contribute to the codebase

* [developing docs](docs/developing.md)

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

### File descriptions

#### documentation

readme.md              - you are reading this!
changelog.md           - major updates are shared here
project-description.md - what this whole thing is about

          docs/    how to develop the software and network
     community/    history and current status of community events and stewardship
      hardware/    how to build your own node
     tutorials/    additional support for installation and usage of the Solar Protocol network
       website/    detailed project history and motivation

#### service code

           dev/    tools for development and running code
           api/    api
      protocol/    the code for having a server participate in the network 
    datalogger/    logs charge controller information

#### data directories - generated files go here

          data/    folder where the point-of-entry log
      frontend/    static website
         local/    local configuration - server name, images, description
