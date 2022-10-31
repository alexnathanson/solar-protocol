"""
Every server runs this script
This collects the photovoltaic data from remote servers via the /charge api endpoint
The purpose of this is minimize the amount of on the fly API calls
"""

# FIXME: I think this was broken - the server i called did not return 4 separate files
# so i think the strip header, reverse and concat didn't do anything?
# regardless, i think the server should just do that concatenation for us

import json
import os
import sys

os.chdir(sys.path[0])  # if this script is called from a different directory


def run():
    print()
    print("***** Running GET Remote Data script *****")
    print()

    # initialize SolarProtocolClass
    solarProtocol = SolarProtocolClass()

    ips = solarProtocol.getDeviceValues("ip")
    names = solarProtocol.getDeviceValues("name")
    macs = solarProtocol.getDeviceValues("mac")

    # get local server name
    myMAC = solarProtocol.getMAC(solarProtocol.MACinterface).strip()
    myName = ""

    for index, mac in enumerate(macs):
        if myMAC == mac:
            myName = nameList[index]
            break

    endpoint = "api/charge?days=4"

    for ip, name in zip(ips, names):
        print(f"{name}: {ip}")
        data = SP.getRequest(f"http://{ip}/{endpoint}")

        if isinstance(data, str):
            print("GET request successful")

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
