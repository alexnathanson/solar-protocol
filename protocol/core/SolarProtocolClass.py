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
from logging import debug, error, info


class SolarProtocol:
    def __init__(self):
        self.localConfigFile = "/local/local.json"
        self.devices = "/data/devices.json"
        # this script retrieves the environmental variables
        self.localConfigData = dict()
        self.loadLocalConfigFile()
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
            error("loadLocalConfigFile error")

    # return the config dictionary
    def getLocalConfigData(self):
        return self.localConfigData

    # returns a specific piece of local config data
    def getLocalConfig(self, key):
        # try to get data from specified key
        try:
            return self.localConfigData[key]
        except:
            error("getLocalConfig error")

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

    def getMAC(self):
        interface = self.localConfigData["interface"]
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(temp_socket.fileno(), 0x8927,  struct.pack('256s', bytes(interface, 'utf-8')[:15]))
        return ':'.join('%02x' % byte for byte in info[18:24])

    def getRequest(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except requests.exceptions.HTTPError:
            exception("HTTP Error")
        except requests.exceptions.Timeout:
            exception("Timeout")
        except:
            exception("Unknown Error")

    """
	returns the specified value from the device list file
	value can be = "ip","mac","time stamp","name","log","tz"
	"""

    def getDeviceValues(self, value):
        with open(self.devices) as file:
            devices = json.load(file)

        values = [device[value] for device in devices]

        return values
