"""
Every server runs this script
This collects the photovoltaic data from remote servers via the /charge-controller api endpoint
The purpose of this is minimize the amount of on the fly API calls
"""

# FIXME: I think this was broken - the server i called did not return 4 separate files
# so i think the strip header, reverse and concat didn't do anything?
# regardless, i think the server should just do that concatenation for us

import json
import os
import sys
from logging import info

os.chdir(sys.path[0])  # if this script is called from a different directory


def run():
    info("***** Running GET Remote Data script *****")

    # initialize SolarProtocolClass
    solarProtocol = SolarProtocolClass()

    ips = solarProtocol.getDeviceValues("ip")
    names = solarProtocol.getDeviceValues("name")
    macs = solarProtocol.getDeviceValues("mac")

    # get local server name
    myMAC = solarProtocol.getMAC()
    myName = ""

    for index, mac in enumerate(macs):
        if myMAC == mac:
            myName = nameList[index]
            break

    for ip, name in zip(ips, names):
        info(f"{name}: {ip}")
        if ip == "127.0.0.1:11221":
            data = solarProtocol.getRequest(f"http://api/api/charge-controller?days=4")
        else:
            data = solarProtocol.getRequest(f"http://{ip}/api/charge-controller?days=4")

        if isinstance(data, str):
            info("GET request successful")

            filename = name.replace(" ", "-").lower()
            with open(f"/data/{filename}.json", "w", encoding="utf-8") as file:
                file.write(data)
                file.close()


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    run()
else:
    consoleOutput = False
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
