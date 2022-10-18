"""
Every server runs this script, which posts its own IP address + other data to:

* all devices in devices.json
* localhost
* solarprotocol.net

Make sure to add DEV to the command when running in development mode
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

headers = {
    #'X-Auth-Key': KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}

isMain = __name__ == "__main__"
DEV = "DEV" in sys.argv

if DEV:
    print("DEV mode")

poeLog = "/data/poe.log"
localConfig = "/home/pi/local/local.json"
deviceList = "/data/devices.json"

newDSTList = []
runningDSTList = []

# this only works with linux
def getmac(interface):
    try:
        mac = open("/sys/class/net/" + interface + "/address").readline()
    except:
        mac = "00:00:00:00:00:00"

    return mac


def getKeys(key):
    with open(deviceList) as file:
        devices = json.load(file)

    return devices.map(lambda device: device[key])


def getPoeLog():
    try:
        file = open(poeLog)
        # take the first 216 lines
        lines = poeFile.readlines()[:216]
        # if solarProtocol.py runs every 10 minutes, there can be max 432 entries
        # this would happen if the current server was POE for the entire 72 hours
        return lines.map(lambda line: line.removeprefix("INFO:root:"))

    except:
        return []

def getLocalKey(key):
    try:
        with open(localConfig) as file:
            device = json.load(file)
            if DEV:
                print(device)
            return device[key]

    except:
        print(f"local config file exception with key {key}")

        if key == "name":
            return "pi"

        if key == "httpPort":
            return ""
'''
Check if is is a new MAC and post if so
If MAC exists check if it is a new IP and post if so
TODO: add timestamp hiearchy here - taking in to account timezones, or using a 24 hour window
'''
# TODO: Check that we aren't doing duplicate work.
# I removed a global for the runningDST list. Seems like a circular dependency? - jedahan
def getNewDST(responses):
    global newDSTList

    macs = getKeys("mac")
    ips = getKeys("ip")

    new_ips = responses.filter(lambda response: response["mac"] not in macs or response["ip"] not in ips) 
    outputToConsole(f"new ips: {new_ips}")

    newDSTList.extend(new_ips)

def postIt(ip, params):
    url = f"http://{ip}/api"
    try:
        response = requests.post(url, headers=headers, params=params, timeout=5)
        if response.ok:
            try:
                getNewDST(response.json())
                print(f"Post to {ip} successful")
            except:
                print(f"Malformatted response from {ip}:")
                print(response.text)
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error", e)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# add a boolean back in if the
def makePosts(ips, api_Key, my_IP, my_Name, my_MAC, my_TZ):
    my_PoeLog = ",".join(getPoeLog())

    global newDSTList

    newDSTList = []

    # all content that the server is posting. API key, timestamp for time of moment, extrenal ip, mac address, name, timezone, poe log
    params = {
        'api_key': str(api_key),
        'stamp': str(time.time()),
        'ip': my_IP,
        'mac': my_MAC,
        'name': my_Name,
        'tz': my_TZ,
        'log': my_PoeLog,
    }

    # post to self automatically
    postIt("localhost:11221", params)

    # exit if we are in debug mode
    if DEV:
        print(params)
        return

    # post to solarprotocol.net
    postIt("solarprotocol.net", params)

    for ip in ips:
        print(f"IP: {ip}")

        # does not work when testing only with local network
        if ip != my_IP:
            postIt(ip, params)

    if len(newDSTList) > 0:
        outputToConsole("New DST list:")
        outputToConsole(newDSTList)
        makePosts(newDSTList, api_Key, my_IP, my_Name, my_MAC, my_TZ)

def getApiKey():
    if DEV:
        return "this-will-fail"

    # We use get_env which reads from a ~/solar-protocol/.spenv to allow 
    # stewards to overwrite environment files from a web interface

    proc = subprocess.Popen(
        ["bash", "/home/pi/solar-protocol/backend/get_env.sh", "API_KEY"],
        stdout=subprocess.PIPE,
    )
    env = proc.stdout.read()

    # convert byte string to string
    env = env.decode("utf-8")

    # remove line breaks
    env = env.replace("\n", "")
    return env

def run():
    print()
    print("***** Running ClientPostIP script *****")
    print()

    myIP = requests.get("https://server.solarpowerforartists.com/?myip").text

    myPort = getLocalKey("httpPort")

    myMAC = getmac("wlan0") # change to eth0 if using an ethernet cable

    myName = getLocalKey("name")

    # only allow alphanumeric, space, and _ characters
    myName = re.sub("[^A-Za-z0-9_ ]+", "", myName)

    # get my timezone
    localHostname = "localhost" if myPort == "" else f"localhost:{myPort}"
    url = f"http://{localHostname}/api"
    myTZ = requests.get(url, params={'systemInfo': 'tz'}).text

    #ips = getKeys("ip")
    ips = ["localhost"]
    remoteHostname = myIP if myPort == "" else f"{myIP}:{myPort}"

    apiKey = getApiKey()
    makePosts(ips, apiKey, remoteHostname, myName, myMAC, myTZ)

def outputToConsole(printThis):
    if consoleOutput:
        print(printThis)

if __name__ == "__main__":
    run()
else:
    consoleOutput = False
