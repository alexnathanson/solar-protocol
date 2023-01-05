"""
Every server runs this script, which posts its own IP address + other data to:

* all devices in devices.json
* localhost
* solarprotocol.net
"""

# these modules are only used by this module within this packages
# all other modules are imported via __init__
import re
from threading import local
import time
import requests
import json
import subprocess
import os
import sys
import fcntl
import socket
import struct
from logging import debug, error, exception, info

from solar_secrets import getSecret, SecretKey


def getMAC():
    interface = getLocal("interface")
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(
        temp_socket.fileno(),
        0x8927,
        struct.pack("256s", bytes(interface, "utf-8")[:15]),
    )
    return ":".join("%02x" % byte for byte in info[18:24])


def getDevices(key: str):
    with open("/data/devices.json") as file:
        devices = json.load(file)
        return [device.get(key) for device in devices]


"""
Truncate the log to the first 216 lines
If solarProtocol.py runs every 10 minutes, there can be max 432 entries
This would happen if the current server was POE for the entire 72 hours
"""


def getPoeLog(filename="/data/poe.log"):
    try:
        with open(filename, "a+") as poeFile:
            lines = poeFile.readlines()
            stripped = [line.rstrip() for line in lines[:216]]
            return ",".join(stripped)
    except:
        exception(f"Could not open {filename}")

    return ","


def getLocal(key):
    defaults = {
        "interface": "wlan0",
        "httpPort": "80",
    }
    default = defaults.get(key)
    try:
        with open("/local/local.json") as file:
            device = json.load(file)
            return device.get(key, default)

    except:
        exception(f"local config file exception with key {key}")


def discoverIps():
    """
    For every device in our local devices.json, ask for their device lists
    For networks under 50 devices, its about 2500 requests roughly every 20 minutes

    TODO: Investigate using epidemic-broadcast-trees a la scuttlebutt
    """

    ips = getDevices("ip")
    macs = getDevices("mac")

    all_devices = []

    for ip in ips:
        devices = requests.get(f"http://{ip}/api/devices").json()
        all_devices.extend(devices)

    info(macs)

    all_macs = {device.get("mac") for device in all_devices}
    local_macs = set(macs)
    new_macs = all_macs - local_macs

    debug(f"new macs: {new_macs}")

    new_devices = [device for device in all_devices if device.get("mac") in new_macs]
    new_ips = [device.get("ip") for device in new_devices]

    info(f"new ips: {new_ips}")

    return new_ips


def postDevice(host: str, data):
    url = f"http://{host}/api/device"

    response = requests.post(url=url, data=data)
    response.raise_for_status()

    info(f"Post to {host} successful")


def publishDevice(hosts: list[str]):
    device = getDevice()
    log = {"log": getPoeLog()}
    networkkey = getSecret(SecretKey.networkkey)

    if networkkey is None:
        error("No network key found, skipping publishDevice")
        return

    metadata = {
        SecretKey.networkkey: networkkey,
        "timestamp": time.time(),
    }

    params = device | log | metadata

    info(params)

    # Since the network is always in flux, exceptions should not stop publishing
    for host in hosts:
        info(f"HOST: {host}")
        try:
            postDevice(host, params)
        except exception:
            error(exception)


def getDevice():
    try:
        ip = requests.get("https://server.solarpowerforartists.com/?myip").text
    except:
        ip = requests.get("https://ifconfig.co").text

    httpPort = getLocal("httpPort")

    mac = getMAC()

    name = getLocal("name")
    # only allow alphanumeric, space, and _ characters
    name = re.sub("[^A-Za-z0-9_ ]+", "", name)

    # get my timezone
    tz = os.environ.get("TZ", "America/New_York")

    return {
        "ip": ip,
        "httpPort": httpPort,
        "mac": mac,
        "name": name,
        "tz": tz,
    }


def run():
    info("***** Running PublishDevice script *****")

    activeIps = ["beta.solarprotocol.net"]
    knownIps = getDevices("ip")
    discoveredIps = discoverIps()

    publishDevice(activeIps + knownIps + discoveredIps)


if __name__ == "__main__":

    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")
    
    run()
