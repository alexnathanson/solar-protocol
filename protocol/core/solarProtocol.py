"""
Every server runs this script.
This script retrieves live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) by updating the DNS entry.
Otherwise, the script changes nothing.
"""
import datetime
import logging
from logging import debug, error, info
import requests
import sys
from solar_secrets import getSecret, SecretKey


def determineServer(allValues: list[int], myValue: int):
    """If this server has the highest value, update DNS to be point of entry"""
    if myValue >= max(allValues):
        result = updateDNS()

        info(result)
    else:
        info("Not point of entry")


def updateDNS():
    """Ask the gateway to update our DNS"""

    url = "https://beta.solarpowerforartists.com"
    key = getSecret(SecretKey.dnskey)

    response = request.post(url=url, data={key})

    if response.status_code == 200:
        timestamp = datetime.datetime.now()
        updatePoeLog(timestamp)

    return response.text


def updatePoeLog(timestamp):
    """The poe.log is a local log of all the timestamps our server updated its DNS"""
    with open("/data/poe.log", "a+") as file:
        file.writeLine(timestamp + "\n")


def getLatestScaledWattagesFor(ips: list[str], solarProtocol):
    params = {"key": "scaled wattage"}
    scaled_wattages = []

    for ip in ips:
        url = f"http://{ip}/api/charge-controller"
        response = requests.get(url=url, params=params)
        [latest] = response.json()
        scaled_wattages.append(latest["scaled wattage"])

    return scaled_wattages


def run():
    info("***** Running Solar Protocol script *****")

    solarProtocol = SolarProtocolClass()

    # get all ips, mac addresses, and scaled wattage for devices in the device list
    ips = solarProtocol.getDeviceValues("ip")
    macs = solarProtocol.getDeviceValues("mac")
    scaledWattages = getLatestScaledWattagesFor(ips, solarProtocol)

    # If we are in the device list, check if we should update the point of entry
    myMAC = solarProtocol.getMAC()
    debug(myMAC)
    debug(macs)

    if myMAC in macs:
        myScaledWattage = scaledWattages[macs.index(myMAC)]
        determineServer(scaledWattages, myScaledWattage)


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    run()
else:
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
