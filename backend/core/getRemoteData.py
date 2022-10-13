"""
Every server runs this script
This collects the PV data from remote servers via the open data API
The purpose of this is minimize the amount of on the fly API calls
"""

"""
1) loop through network devices
	2) get most recent 4 files, if call is successful:
		3) strip headers and merge into 1 file organized by time (scale by tz???)
		4) save file
"""

import json
import os
import sys

os.chdir(sys.path[0])  # if this script is called from a different directory

fileDst = "/home/pi/local/data/"


def run():
    print()
    print("***** Running GET Remote Data script *****")
    print()

    # initialize SolarProtocolClass
    SP = SolarProtocolClass()

    ips = SP.getDeviceValues("ip")
    names = SP.getDeviceValues("name")
    macs = SP.getDeviceValues("mac")

    # get local server name
    myMAC = SP.getMAC(SP.MACinterface).strip()
    myName = ""

    for index, mac in enumerate(macs):
        if myMAC == mac:
            myName = nameList[index]
            break

    # This must be V1 else an error occurs - must update the handleData function to use V2
    endpoint = "/api/v1/opendata.php?day=4"

    for ip, name in zip(ips, names):
        print(name + ": " + ip)
        if name == myName:
            # this probably to be updated to handled irregular ports...
            data = SP.getRequest(f"http://localhost/{endpoint}")
        else:
            data = SP.getRequest(f"http://{ip}/{endpoint}")

        if isinstance(data, str):
            print("GET request successful")

            # remove spaces and make all lower case
            handleData(data, name.replace(" ", "").lower())


# repackage data starting from most recent
# strip headers, combine all 4 files into 1, save file
def handleData(ccFiles, name):
    combinedFile = []

    ccFiles = json.loads(ccFiles)

    for file in ccFiles:
        headers = file.pop(0)

        for l in reversed(file):
            combinedFile.append(l)

    # add headers back
    combinedFile.insert(0, headers)

    with open(fileDst + name + ".json", "w", encoding="utf-8") as file:
        file.write(json.dumps(combinedFile))
        file.close()


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    run()
else:
    consoleOutput = False
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
