"""
Every server runs this script, which

Retrieves live PV power (watts) data from other servers.
Identifies the device producing the most power at the moment.
Updates the dns to become the Point of Entry if it is producing the most power.

Otherwise, the script changes nothing.
"""
import datetime
import logging
from logging import debug, error, info
import requests
import os
from solar_common.secrets import getSecret, SecretKey


def determineServer(allValues: list[int], myValue: int):
    """If this server has the highest value, update DNS to be point of entry"""
    if myValue >= max(allValues):
        info("Point of entry")
        updateDNS()
    else:
        info("Not point of entry")


def updateDNS() -> str:
    """Ask the gateway to update our DNS"""

    url = "http://beta.solarpowerforartists.com/api/update"
    key = getSecret(SecretKey.dnskey)

    response = requests.post(url=url, data={"key": key})

    if response.status_code == 200:
        timestamp = datetime.datetime.now()
        updatePoeLog(timestamp)
    else:
        error(f"{response=}")

    return response.text


def updatePoeLog(timestamp):
    """The poe.log is a local log of all the timestamps our server updated its DNS"""
    with open("/data/poe.log", "a") as file:
        file.write(f"{timestamp}\n")


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
    MAC = os.environ.get("MAC")
    debug(f"{MAC=}")

    if MAC in macs:
        myScaledWattage = scaledWattages[macs.index(MAC)]
        determineServer(scaledWattages, myScaledWattage)


if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass

    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")

    run()
else:
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
