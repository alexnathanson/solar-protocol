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
from logging import error, exception, info

from solar_secrets import getSecret, SecretKey

poeLog = "/data/poe.log"
localConfig = "/local/local.json"
deviceList = "/data/devices.json"


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
    with open(deviceList) as file:
        devices = json.load(file)
        return [device.get(key) for device in devices]


def getPoeLog():
    try:
        file = open(poeLog)
        # take the first 216 lines
        lines = poeFile.readlines()[:216]
        # if solarProtocol.py runs every 10 minutes, there can be max 432 entries
        # this would happen if the current server was POE for the entire 72 hours
        poeLog = [line.removeprefix("INFO:root:") for line in lines]
        return ",".join(poeLog)

    except:
        return ""


def getLocal(key):
    defaults = {
        "interface": "wlan0",
        "httpPort": "80",
    }
    default = defaults.get(key)
    try:
        with open(localConfig) as file:
            device = json.load(file)
            return device.get(key, default)

    except:
        exception(f"local config file exception with key {key}")


"""
For every device in our local devices.json, ask for their device lists
For networks under 50 devices, its about 2500 requests roughly every 20 minutes

TODO: Investigate using epidemic-broadcast-trees a la scuttlebutt
"""


def discoverIps():
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

    new_devices = [device for device in all_devices if device.get("mac") in new_macs]
    new_ips = [device.get("ip") for device in new_devices]

    info(f"new ips: {new_ips}")

    return new_ips


def postDevice(ip, data):
    url = f"http://{ip}/api/device"

    try:
        response = requests.post(url=url, data=data, timeout=5)
        if response.ok:
            info(f"Post to {ip} successful")
        else:
            error(f"Malformed response from {ip}")
            error(response.json())
    except json.decoder.JSONDecodeError:
        exception(f"JSON Decode Error")
    except requests.exceptions.HTTPError:
        exception(f"Http Error")
    except requests.exceptions.ConnectionError:
        exception(f"Connection Error")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


def publishDevice(ips):
    device = getDevice()
    log = {"log": getPoeLog()}

    metadata = {
        "apiKey": getApiKey(),
        "timestamp": time.time(),
    }

    params = device | log | metadata

    info(params)

    for ip in ips:
        info(f"IP: {ip}")
        postDevice(ip, params)


"""
TODO: We should talk about what the apiKey is used for, and having different keys for each device
"""


def getApiKey():
    return getSecret(SecretKey.apiKey)


def getDevice():
    # FIXME: should we remove server. to make fully p2p?
    try:
        ip = requests.get("http://server.solarprotocol.com/?myip").text
    except:
        ip = "127.0.0.1"

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

    selfIps = ["api:11221"]
    activeIps = ["beta.solarprotocol.net"]
    knownIps = getDevices("ip")
    discoveredIps = discoverIps()

    # publishDevice(selfIps + activeIps + knownIps + discoveredIps)
    publishDevice(selfIps)


def outputToConsole(message):
    if consoleOutput:
        info(message)


if __name__ == "__main__":
    run()
else:
    consoleOutput = False
