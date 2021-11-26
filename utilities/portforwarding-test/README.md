# Port forwarding test

Port forwarding is a crucial component of Solar Protocol. It is what allows an external device to talk to your server on your local private network. <strong>If your hardware is being purchased and/ or shipped to you by Solar Protocol you must check that your network can properly enable port forwarding before we send you any hardware.</strong> If you are purchasing your own hardware, we strongly recommended that you test that port forwarding is possible first to avoid wasting your money.

While there are work arounds if your ISP or hardware doesn't allow for port forwarding, we generally want avoid complex routing or tunneling because we want to minimize the amount of hardware not running directly off of solar power.

### How do IPs work?
Every local area network (LAN) assigns IP addresses to all the networked devices on the local private network. The ISP assigns a public IP to your...

Set the test device to a static IP. This will ensure that the device's local IP wont change. The Solar Protocol network is designed to allow dynamic public IPs. A public IP is the IP address used by external devices to communicate with your local area network (LAN). However, it will not work with dynamic private IPs i.e. 

## Testing device

For this test to work, you must set up a simple server to serve a basic HTML page. We also recommend that you enable SSH on the server to enable that test. However, we have not found any instances (yet) where portforwarding works for html but not for ssh, so if you can't run test 1B, you should be fine. 

We recommend you use a Raspberry Pi, which is the computer Solar Protocol uses for our servers. This will allow you to test both the html and ssh ports in exactly the same way we will be using the devices when it is connected to the network. If you are using a Raspberry Pi, go ahead an install the Solar Protocol software. For this test, you should not enable the scripts via crontab. It can also run off of grid power for this test.

If you are using another type of device to run this test (like your laptop or desktop computer), you can spin up a server quickly with the following commands:

## Set static IP and enable port forwarding on your router

Every router is different, which makes providing instructions difficult.

The typical process goes something like this:
* log in to your router
* navigate to the 

1) Set local static IP


2) Set ports

Default ports 80 for html and 22 for ssh

Our systems is capable of working with other ports, however

## Test your portforwarding settings

There are 2 ways to test that your portforwarding settings are working properly. You must do both tests.

1) Access your ports directly

It is crucial that you run this test from a device not on your local network. One easy way to do this is through your smart phone. Make sure your device is using cell network data and is not on wifi. Alternatively, you can connect to a completely different network and try to connect to your server. If necessary, ask one of the members of Solar Protocol to attemp to access your test site.

a) In a browser, go to your public IP address

If you aren't sure what your public IP address is you can find it by going to https://www.myip.com/

If you are weren't able to use port 80, you will have to append your IP address with the port like this:<br>
` 8.8.8.8:1000` In this example `8.8.8.8` is the IP address which is followed by a `:` and then the port number which is `1000`

b) SSH in to your device

2) Testing tools

There are a number of online tools available that can confirm your ports are open. Either of these will work:

* https://portchecker.co/
* https://www.yougetsignal.com/tools/open-ports/

Run this test on both your http and ssh ports. If you were not able to use the default ports (80 & 22) you must manually enter the port number when you run the test. The tester will tell you if the ports are open or closed.

## Troubleshooting

1) Does your ISP allow for portforwarding?

Not every internet service provider (ISP) allows for portforwarding on every type of network. 