# Port forwarding test

Port forwarding is a crucial component of Solar Protocol. It is what allows an external device to communicate with your server on your local private network. <strong>If your hardware is being purchased and/ or shipped to you by Solar Protocol you must confirm that your network can properly enable port forwarding before we send you any hardware.</strong> If you are purchasing your own hardware, we strongly recommended that you test that port forwarding is possible first to avoid wasting your money.

While there are work arounds if your ISP or hardware doesn't allow for port forwarding, we generally want avoid complex routing or tunneling to minimize the amount of hardware not running directly off of solar power.

This test is for residential and small scale commercial networks. It requires that you log in to your networking hardware to make the necessary changes. If you are on a large commerical network, you will likely need to consult with your IT department.

## 1) Set static IP and enable port forwarding on your router

Every router is different, which makes providing instructions difficult. These settings are found on your router's web interface, which can be accessed via a browser. To access your router's interface you will need to know the default gateway address for your network. The default gateway address is an IP address for your router. Some routers also have a conveniant URL. The easiest way to find this address is usually via your computer's network settings. Instructions for finding your default gateway address from your computer's network settings can be found at https://www.lifewire.com/how-to-find-your-default-gateway-ip-address-2626072. This information might also be found on a sticker on the router or in the router hardware manual. If all else fails, you may need to contact your ISP to find out. Once you have logged in to the router's control panel follow the steps below.

### 1.1) Set local/private static IP

Your public IP address is assigned by your ISP. A public IP is the IP address used by external devices to communicate with devices on your local area network (LAN). Your private LAN IP is assigned by your router either automatically through DHCP or manually. IPs set with DHCP change periodically, so we need to manually assign a static IP to the device our server is running on. This will ensure that the device's local IP wont change. The Solar Protocol network is designed to allow dynamic public IPs, so it is not a problem if your ISP changes your public IP. 

A static IP can be set via the device being connected to the network (in our case the Raspberry Pi) or by the router. If you are setting a static IP on the device, make sure that you choose an IP address outside of the DHCP range of your router. It is important to ensure that the same IP address isn't used by multiple devices simultaneously. For this reason, we recommend keeping the Raspberry Pi set to DHCP and setting the static IP via the router's interface.

* Make sure that the device you want to set is on the network
* Access your router's interface
* Locate the list of devices currently on the network. This section might be called "client devices", "connected devices", "dhcp assignments", "dhcp reservations", or something similar.
	* All the devices on your network that use DHCP will be listed. Locate your device in this list.  
* Look for a way to reserve a particular IP address or assign an IP address to a particular device.
* If you are able to reserve an IP address, choose the IP address that your device is currently assigned. It is crucial that you dont assign your server an IP address already in use by another device. If you can't reserve an IP address currently used for DHCP, make sure to select an IP address outside of the DHCP range that isn't being used by anything else. On some networks there are blocks of IPs that are explicity reserved for static use.

### 1.2) Set ports

* Access your router's interface
* Locate the port forwarding settings
	* This is often under the Advanced tab.
* Enable port forwarding
	* Typically, you must enter a name for your device, specify the IP address, and the port that will be forwarded.
	* The standard ports we use are 80 for HTTP and 22 for SSH. If those ports aren't available because they are being used by something else on your network or by the router itself, you can choose different ports.
	* You will likely need to make 2 seperate entries for each of the ports that will be forwarded.

## 2) Test your port forwarding settings

There are 2 tests that you should conduct for both HTTP and SSH

### 2.1) Online testing tools

There are a number of online tools available that can confirm whether your ports are open. Either of these will work:

* https://portchecker.co/
* https://www.yougetsignal.com/tools/open-ports/
* https://www.portchecktool.com/

Run this test on both your http and ssh ports. If you were not able to use the default ports (80 & 22) you must manually enter the port number when you run the test. The tester will tell you if the ports are open or closed.

### 2.2) Serve HTML content and SSH into your server

It is crucial that you run these tests from a device not on your local network. One easy way to do this is through your smart phone. Make sure your phone is using cell network data and is not on wifi. Alternatively, you can connect to a completely different network and try to connect to your server. If necessary, ask one of the members of Solar Protocol to attemp to access your test site remotely.

#### 2.2.1) Go to your web page in a browser

For this test to work, you must set up a server to serve HTML content. See the instructions below to create a server for testing.  

If you aren't sure what your public IP address is you can find it by going to https://www.myip.com/

If you are weren't able to use port 80, you will have to append your IP address with the port like this:<br>
` 8.8.8.8:1000` In this example `8.8.8.8` is the IP address which is followed by a `:` and then the port number which is `1000`

#### 2.2.2) SSH in to your device

If you are using a Raspberry Pi, you should definitely complete this step. If you are using a Windows device it may be difficult to enable SSH. We have not found any instance (yet) where port forwarding works for HTTP but not for SSH, so if you are using a computer that doesn't easily let you SSH in to it and you can't run test this test you should be fine assuming the other 3 tests were successful. 

## 3) Disable port forwarding

Once the tests have been successfully completed, do not leave port forwarding enabled unless you have the proper security measures in place. Go back through step 1 and disable both HTTP and SSH port forwarding.

## Create a server for testing

We recommend you use a Raspberry Pi, which is the computer Solar Protocol uses for our servers. This will allow you to test both the html and ssh ports in exactly the same way we will be using the devices when it is connected to the network.

There are many ways to spin up a server. Follow these instructions to create a Python server.

* If you dont already have Python, you can install it from https://www.python.org/
	* To check if you already have python installed, run this command in terminal: `python --version` or if that command fails try `python3 -V`
* We will be serving the index.html file in the portforwarding-test directory
	* Either download the entire repository or just the index.html file found at https://github.com/alexnathanson/solar-protocol/blob/master/utilities/portforwarding-test/index.html.
* In terminal, navigate to the location of that index file.
* Check which version of Python you are running by typing this command in terminal:`python --version` or if that command fails try `python3 -V`
* Start the server (if you are using a port other than 80 for HTML replace `80` below with your actual port number)
	* If you are running Python2 enter this command to start your server: `python -m SimpleHTTPServer 80`
	* If you are running Python3 enter this command to start your server: `python -m http.server 80` or `python3 -m http.server 80` or `py -3 -m http.server 80`
* Test your server by opening up a browser and going to `http://localhost:80`

## Troubleshooting

### Does your ISP allow port forwarding?

Not every internet service provider (ISP) allows for port forwarding. If you can't find your port forwarding settings in the router interface or they appear to be locked, call your ISP to check whether they allow port forwarding. 