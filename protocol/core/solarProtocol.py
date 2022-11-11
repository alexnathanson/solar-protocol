"""
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
"""
import datetime
import logging
import sys
from solar_secrets import getSecret, SecretKey

DEV = "DEV" in sys.argv


def determineServer(allValues, myValue, solarProtocol):
    """
    If this server has the highest value, update DNS to be point of entry
    """
    if myValue > max(allValues):
        print("Point of entry")

        logging.info(datetime.datetime.now())

        # Do not update DNS if running in DEV
        secretkey = SecretKey.dnsPassword
        key = "this-will-fail" if DEV else getSecret(secretkey)
        result = solarProtocol.updateDNS(solarProtocol.myIP, key)
        print(result)
    else:
        print("Not point of entry")


def getLatestScaledWattagesFor(ips: list[str], solarProtocol):
    scaled_wattages = [
        solarProtocol.getRequest(f"http://{ip}/charge?key='scaled wattage'")
        for ip in ips
    ]
    return [latest.pop()["scaled wattage"] for latest in scaled_wattages]


def run():
    print()
    print("***** Running Solar Protocol script *****")
    print()

    solarProtocol = SolarProtocolClass()

    logging.basicConfig(filename="/data/poe.log", level=logging.INFO)

    # get all ips, mac addresses, and apiValues for devices in the device list
    ips = solarProtocol.getDeviceValues("ip")
    macs = solarProtocol.getDeviceValues("macs")
    scaledWattages = getLatestScaledWattagesFor(ips, solarProtocol)

    # If we are in the device list, check if we should update the point of entry
    myMAC = solarProtocol.getMAC(solarProtocol.MACinterface)
    if myMAC in macs:
        myScaledWattage = scaledWattages[macs.index(myMAC)]
        determineServer(scaledWattages, myScaledWattage, solarProtocol)


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    run()
else:
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
