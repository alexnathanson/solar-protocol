"""
Every server runs this script, which posts its own IP address + other data to:

* all devices in devices.json
* localhost
* solarprotocol.net
"""

import re
import time
import requests
import json
import os
from logging import debug, error, exception, info

from ../../common.secrets import getSecret, SecretKey


def getDevices(key: str):
    filename = "../../data/devices.json"
    try:
        with open(filename) as file:
            devices = json.load(file)
            return [device.get(key) for device in devices]
    except FileNotFoundError:
        with open(filename, "w") as file:
            json.dump([], file)
            return []


def getPoeLog(filename="../../data/poe.log"):
    """
    Truncate the log to the first 216 lines
    If solarProtocol.py runs every 10 minutes, there can be max 432 entries
    This would happen if the current server was POE for the entire 72 hours
    """
    try:
        with open(filename, "a+") as poeFile:
            lines = poeFile.readlines()
            stripped = [line.rstrip() for line in lines[:216]]
            return stripped
    except FileNotFoundError:
        with open(filename, "w") as poeFile:
            poeFile.write("")
            return []

    return []


def getLocal(key):
    defaults = {
        "interface": "wlan0",
        "httpPort": "80",
    }
    default = defaults.get(key)
    try:
        with open("../../local/local.json") as file:
            device = json.load(file)
            return device.get(key, default)
    except Exception:
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

    debug(f"{new_macs=}")

    new_devices = [device for device in all_devices if device.get("mac") in new_macs]
    new_ips = [device.get("ip") for device in new_devices]

    info(f"{new_ips=}")

    return new_ips


def postDevice(host: str, data):
    url = f"http://{host}/api/device"
    debug(f"{data=}")

    response = requests.post(url=url, data=data)
    if not response.ok:
        body = response.text
        debug(f"{body=}")
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
        except Exception as exception:
            error(exception)


def getDevice():
    try:
        ip = requests.get("https://server.solarpowerforartists.com/?myip").text
    except Exception:
        ip = requests.get("https://ifconfig.co/ip").text.strip()

    httpPort = getLocal("httpPort")

    mac = os.environ.get("MAC")

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

    # On start, devices.json is empty
    # So we publish to ourselves, to populate it
    # Since we cannot know a priori a nodes information

    selfIps = ["api"]
    activeIps = ["beta.solarprotocol.net"]
    knownIps = getDevices("ip")
    discoveredIps = discoverIps()

    publishDevice(selfIps + activeIps + knownIps + discoveredIps)


if __name__ == "__main__":
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")

    run()
