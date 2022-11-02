"""
this class handles some common core functionality for the Solar Protocol project
including:
retrieving data from local config
retrieving local environmental variables
getting own MAC address
getting own public IP address
managing DNS gateway endpoints (updating and returning white/black lists)

future additions:
retrieving live and historic data from charge controller
load and retrieve deviceList file

currently this class only handles some new functionality for solarProtocol.py.
Refactoring and expansion is required to create additional methods and apply this to publishDevice.py too
"""

import requests
import json
import subprocess
import sys
import os


class SolarProtocol:
    def __init__(self):
        self.localConfigFile = "/local/local.json"
        self.devices = "/data/devices.json"
        # this script retrieves the environmental variables
        self.localConfigData = dict()
        self.loadLocalConfigFile()
        self.myIP = requests.get("http://server.solarpowerforartists.com/?myip").text
        # dns.solarprotocol.net isn't redirecting properly so we're using the below url for the time being
        self.dnsURL = "https://server.solarpowerforartists.com/"
        self.MACinterface = "wlan0"  # this should be wlan0 even if using ethernet, because its used for identifying hardware regardless of how the connection is made...

    # load in data from config file
    def loadLocalConfigFile(self):
        try:
            with open(self.localConfigFile) as locFile:
                locData = json.load(locFile)
                for key, value in locData.items():
                    # store data
                    self.localConfigData[key] = value
        except:
            print("loadLocalConfigFile error")

    # return the config dictionary
    def getLocalConfigData(self):
        return self.localConfigData

    # returns a specific piece of local config data
    def getLocalConfig(self, key):
        # try to get data from specified key
        try:
            return self.localConfigData[key]
        except:
            print("getLocalConfig error")

            if key == "name":
                return "pi"
            elif key == "httpPort":
                # should this return 80 as a default?
                return ""

    """
	Returns the scaling factor for the module based on a standard of 50 watts
	(i.e. if a server is using a 100 watt module, it must be divided by 2,
	and if it is using a 25 watt module it must by multiplied by 2)
	In the future a more complex method that takes in to account I-V curves may need to be applied
	"""

    def pvWattsScaler(self):
        try:
            return 50.0 / float(self.localConfigData["pvWatts"])
        except:
            return 1

    # returns the device's MAC address at the specified interface
    # this only works with linux
    def getMAC(self, interface):
        try:
            mac = open(f"/sys/class/net/{interface}/address").readline()
        except:
            mac = "00:00:00:00:00:00"

        return mac

    def getRequest(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.Timeout as err:
            print(err)
        except err:
            print(err)

    # returns the url with parameters for updating the DNS via a GET request
    def updateDNS(self, ip, key):
        return f"{self.dnsURL}?ip={ip}&key={key}"

    """
	returns the specified value from the device list file
	value can be = "ip","mac","time stamp","name","log","tz"
	"""

    def getDeviceValues(self, value):
        with open(self.devices) as file:
            devices = json.load(file)

        values = [device[value] for device in devices]

        return values
