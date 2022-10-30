# How does Solar Protocol work?

The Solar Protocol website is served from whichever server is in the most sunlight at a given time. We call this server the active server. The active server is determined through a series of programs that each server runs and protocols that they use to communicate with one another. This process is broken down in more detail below.

## Collecting Electrical Data

Every few minutes each individual server logs its own electrical data. This data includes solar panel output, battery status, and energy consumption stats. This is done through communicating with a device called a charge controller. The charge controller is responsible for safely charging the battery from the solar panel. The specific charge controller we use was chosen because it has a communication protocol that we can send and retrieve data from.

## Determing Active Server Status

There are a number of other pieces of software (called scripts) that run in the background on Solar Protocol servers. The frequency of these processes is based on the available energy. This means that when power is more plentiful we run them more often.

One of these scripts is responsible for determining if it is producing the most power. This entails requesting solar power data from all the other servers in the network via the API. The results of the API request are compared against its own data and if it is producing the most power it determines it is the active server. (In instances where servers have different size solar arrays we scale them down to a 50W module.)

If the server is active, another API call is made to update the DNS and point the URL to the server's IP address. The DNS system is like an automated phone book for the internet. It is what enables your browser to get the content you expect when you go to a particular website. In our case solarprotocol.net is our URL, but that is really just a convienant name that is easy to remember. The IP address is really the location where the resources that make up our website can be found. This all happens convienantly behind the scenes whenever you go to any website.

If the server determines that it is not the active server, because another server on the network is producing more power than it, it does nothing. This helps avoid conflicts between servers. Also, because each server has the autonomy to make this decision on its own it is resilient and will continue to function even if many servers are offline.