"""
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
"""
import datetime
import logging
from logging import error, info
import sys
from solar_secrets import getSecret, SecretKey


def determineServer(allValues, myValue):
    """
    If this server has the highest value, update DNS to be point of entry
    """
    if myValue > max(allValues):
        info(f"Point of entry {datetime.datetime.now()}")

        # TODO: allow overwriting host and domain in local.json
        result = updateDNS()

        info(result)
    else:
        info("Not point of entry")


# TODO: we should probably sanitize this name
def getName():
    filename = f"/local/local.json"

    with open(filename, "r") as jsonfile:
        localData = json.load(jsonfile)
        return localData["name"]

    error("Problem finding name")


def updateDNS(host: str = "beta", domain: str = "solarprotocol.net"):
    password = getSecret(SecretKey.dnsPassword)

    params = {host, domain, password}
    url = "https://dynamicdns.park-your-domain.com/update"

    response = request.get(url=url, params=params)

    if response.status == 200:
        name = getName()
        updatePoeLog(name, ip)

    return response.text


def getLatestScaledWattagesFor(ips: list[str], solarProtocol):
    scaled_wattages = [
        solarProtocol.getRequest(f"http://{ip}/charge?key='scaled wattage'")
        for ip in ips
    ]
    info(scaled_wattages)
    info("tried to get latest")
    return [latest["scaled wattage"] for latest in scaled_wattages]


def run():
    info("***** Running Solar Protocol script *****")

    solarProtocol = SolarProtocolClass()

    logging.basicConfig(filename="/data/poe.log", level=logging.INFO)

    # get all ips, mac addresses, and apiValues for devices in the device list
    ips = solarProtocol.getDeviceValues("ip")
    macs = solarProtocol.getDeviceValues("mac")
    scaledWattages = getLatestScaledWattagesFor(ips, solarProtocol)

    # If we are in the device list, check if we should update the point of entry
    myMAC = solarProtocol.getMAC(solarProtocol.MACinterface)
    if myMAC in macs:
        myScaledWattage = scaledWattages[macs.index(myMAC)]
        determineServer(scaledWattages, myScaledWattage)


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    run()
else:
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
