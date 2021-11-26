# Port forwarding test

Port forwarding is a crucial component of Solar Protocol. If your hardware is being purchased and/ or shipped to you by Solar Protocol you must check that your network can properly enable port forwarding before we send you any hardware. If you are purchasing your own hardware, we strongly recommended that you test that port forwarding is possible to avoid wasting your money.

## Testing device

In order to test this, you must create a server. The best way to do this is with a Raspberry Pi, which is what we are using for the servers in Solar Protocol. This will allow you to test both the html and ssh ports.

## Set static IP and enable port forwarding on your router

Every router is different, which makes providing instructions difficult.

The typical process goes something like this:
* log in to your router
* navigate to the 

1) Set local static IP

### How do IPs work?
Every local area network (LAN) assigns IP addresses to all the networked devices on the local private network. The ISP assigns a public IP to your...

Set the test device to a static IP. This will ensure that the device's local IP wont change. The Solar Protocol network is designed to allow dynamic public IPs. A public IP is the IP address used by external devices to communicate with your local area network (LAN). However, it will not work with dynamic private IPs i.e. 

2) Set ports

Default ports 80 for html and 22 for ssh

Our systems is capable of working with other ports, however

## Test your portforwarding settings

There are 2 ways to test that your portforwarding settings are working properly. You must do both tests.

1) Access your ports directly

It is crucial that you run this test from a device not on your local network. One easy way to do this is through your smart phone. Make sure your device is using cell network data and is not on wifi. Alternatively, you can connect to a completely different network and try to connect to your server. If necessary, ask one of the members of Solar Protocol to attemp to access your test site.

a) In a browser, go to your public IP address

If you are weren't able to use port 80, you will have to append your IP address with the port like this:<br>
` 8.8.8.8:1000` In this example `8.8.8.8` is the IP address which is followed by a `:` and then the port number which is `1000`

b) SSH in to your device

2) Testing tools

There are a number of online tools available that can confirm your ports are open.

* https://portchecker.co/
* https://www.yougetsignal.com/tools/open-ports/

Run this test on both your http and ssh ports

## Troubleshooting

1) Does your ISP allow for portforwarding?

Not every internet service provider (ISP) allows for portforwarding on every type of network. 