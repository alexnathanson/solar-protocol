"""
Every server runs this script.
This script retreives live PV power (watts) data from other servers.
Compares data between devices and identifies the device producing the most power at the moment.
If the local device is producing the most power, it becomes the Point of Entry (PoE) and updates the DNS system.
Otherwise, the script changes nothing.
"""
import datetime
import logging
from logging import debug, error, info
import requests
import sys
from solar_secrets import getSecret, SecretKey


def determineServer(allValues: list[int], myValue: int):
    """
    If this server has the highest value, update DNS to be point of entry
    """
    if myValue >= max(allValues):

        # TODO: allow overwriting host and domain in local.json
        result = updateDNS()

        info(result)
    else:
        info("Not point of entry")


# TODO: we should probably sanitize this name
def getName():
    try:
        with open("/local/local.json", "r") as jsonfile:
            localData = json.load(jsonfile)
            return localData["name"]
    except KeyError:
        error(f"Problem finding name")


"""
Fully peer-to-peer = each machine keeps the secret locally
FIXME: We should discuss this
"""


def updateDNS(host: str = "beta", domain: str = "solarprotocol.net"):
    password = getSecret(SecretKey.dnsPassword)

    params = {host, domain, password}
    url = "https://dynamicdns.park-your-domain.com/update"

    response = request.get(url=url, params=params)

    if response.status_code == 200:
        timestamp = datetime.datetime.now()
        # name = getName()
        # updateDnsLog(name, ip, timestamp)
        updatePoeLog(timestamp)

    return response.text


"""
The dns.log is meant to be for the 'gateway' server
All requests used to update DNS go through the gateway
Which gave us a nice centralized list of server names/ips/timestamps

FIXME: have a discussion about this
"""


def updateDnsLog(name: str, ip: str, timestamp):
    with open("/data/dns.log", "a+", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[name, ip, timestamp])
        writer.writerow([name, ip, timestamp])


"""
The poe.log is a local log of all the timestamps our server updated its DNS
"""


def updatePoeLog(timestamp):
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
