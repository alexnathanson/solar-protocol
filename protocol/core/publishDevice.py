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
    info = fcntl.ioctl(temp_socket.fileno(), 0x8927,  struct.pack('256s', bytes(interface, 'utf-8')[:15]))
    return ':'.join('%02x' % byte for byte in info[18:24])


def getDevices(key: str):
    with open(deviceList) as file:
        devices = json.load(file)

    return [device[key] for device in devices]


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
    try:
        with open(localConfig) as file:
            device = json.load(file)
            if key in device:
                return device[key]
            if key in defaults:
                return defaults[key]

    except:
        exception(f"local config file exception with key {key}")


"""
For every device in our local devices.json, ask for their device lists
FIXME: lets discuss exactly how chatty this is
"""


def discoverIps():
    ips = getDevices("ip")
    macs = getDevices("mac")

    all_devices = []

    for ip in ips:
        devices = requests.get(f"http://{ip}/api/devices").json()
        all_devices.append(devices)

    all_macs = {device["mac"] for device in all_devices}
    local_macs = {macs}

    new_macs = all_macs - local_macs
    new_devices = {all_devices.filter(lambda device: device["mac"] in new_macs)}

    outputToConsole(f"new ips: {[ device['ip'] for device in new_devices ]}")

    discoveredIps = [device["ip"] for device in newDevices]

    return discoveredIps


def postDevice(ip, params):
    url = f"http://{ip}/api/device"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(url=url, headers=headers, params=params, timeout=5)
        if response.ok:
            info(f"Post to {ip} successful")
        else:
            error(f"Malformatted response from {ip}: {response.text}")
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


def publishDevice(ips, device, log):
    metadata = {
        "apiKey": getApiKey(),
        "timestamp": time.now(),
    }

    params = device | log | metadata

    for ip in ips:
        info(f"IP: {ip}")
        postDevice(ip, params)


def getApiKey():
    return getSecret(SecretKey.apiKey)


def getDevice():
    # FIXME: should we remove server. to make fully p2p?
    ip = requests.get("https://server.solarpowerforartists.com/?myip").text
    httpPort = getLocal("httpPort")

    mac = getMAC()

    name = getLocal("name")
    # only allow alphanumeric, space, and _ characters
    name = re.sub("[^A-Za-z0-9_ ]+", "", name)

    # get my timezone
    tz = os.environ["TZ"] if "TZ" in os.environ else "America/New_York"

    log = getPoeLog()

    return {
        "ip": ip,
        "httpPort": httpPort,
        "mac": mac,
        "name": name,
        "tz": tz,
        "log": log,
    }


def run():
    info("***** Running PublishDevice script *****")

    apiKey = getApiKey()
    device = getDevice()

    knownIps = getDevices("ip")
    selfIp = "localhost:11221"
    activeIp = "solarprotocol.net"
    discoveredIps = discoverIps()

    # post to self
    publishDevice([selfIp], apiKey, device)

    # post to solarprotocol.net
    publishDevice([activeIp], apiKey, device)

    # post to known ips
    publishDevice(knownIps, apiKey, device)

    # post to discovered ips
    publishDevice(discoveredIps, apiKey, device)


def outputToConsole(message):
    if consoleOutput:
        info(message)


if __name__ == "__main__":
    run()
else:
    consoleOutput = False
