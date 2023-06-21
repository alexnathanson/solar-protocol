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

Refactoring and expansion is required to create additional methods,
and apply this to publishDevice.py too
"""

import json
from logging import error


class SolarProtocol:
    def __init__(self):
        self.localConfigFile = "/local/local.json"
        self.devices = "/data/devices.json"
        # this script retrieves the environmental variables
        self.localConfigData = dict()
        self.loadLocalConfigFile()

    # load in data from config file
    def loadLocalConfigFile(self):
        try:
            with open(self.localConfigFile) as locFile:
                locData = json.load(locFile)
                for key, value in locData.items():
                    # store data
                    self.localConfigData[key] = value
        except Exception:
            error("loadLocalConfigFile error")

    # return the config dictionary
    def getLocalConfigData(self):
        return self.localConfigData

    # returns a specific piece of local config data
    def getLocalConfig(self, key):
        # try to get data from specified key
        try:
            return self.localConfigData[key]
        except Exception:
            error("getLocalConfig error")

            if key == "name":
                return "pi"
            elif key == "httpPort":
                # should this return 80 as a default?
                return ""

    def pvWattsScaler(self):
        """
        Returns the scaling factor for the module based on a standard of 50 watts
        (i.e. if a server is using a 100 watt module, it must be divided by 2,
        and if it is using a 25 watt module it must by multiplied by 2)
        TODO: apply a more complex method that takes in to account I-V curves
        """
        try:
            return 50.0 / float(self.localConfigData["pvWatts"])
        except Exception:
            return 1

    def getDeviceValues(self, value):
        """
        returns the specified value from the device list file
        value can be = "ip","mac","time stamp","name","log","tz"
        """
        try:
            with open(self.devices) as file:
                devices = json.load(file)

            values = [device[value] for device in devices]

            return values
        except FileNotFoundError:
            with open(self.devices, "w") as file:
                json.dump([], file)
                return []
        except KeyError as key:
            raise Exception(f"Missing {key=} from device entry")
