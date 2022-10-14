"""
Every server runs this script, which posts its own IP address + other data to:

* all devices in deviceList.json
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
DEV = os.environ.get("ENV") == "DEV" or "DEV" in sys.argv

if DEV:
    print("Dev mode")

poeLog = "/home/pi/solar-protocol/backend/data/poe.log"
localConfig = "/home/pi/local/local.json"
deviceList = "/home/pi/solar-protocol/backend/data/deviceList.json"

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
        return [0]

def getLocalKey(key):
    try:
        with open(localConfig) as file:
            device = json.load(file)
            return device[key]

    except:
        print(f"local config file exception with key {key}")

        if key == "name":
            return "pi"

        if key == "httpPort":
            return ""

def getNewDST(responseList):
    global newDSTList, runningDSTList
    # check if is is a new MAC and post if so
    # if type(responseList) == list:
    # if MAC exists check if it is a new IP and post if so (maybe compare time stamps accounting for time zone)
    for r in responseList:
        # print(r['mac'])

        if r["mac"] not in getKeys("mac"):
            if r["ip"] not in runningDSTList:
                outputToConsole("new ip: " + r["ip"])
                newDSTList.append(r["ip"])
                runningDSTList.append(r["ip"])
        elif r["ip"] not in getKeys("ip"):
            # in the future add in a time stamp heirchy here - taking in to account timezones (or use a 24 hours window)
            if r["ip"] not in runningDSTList:
                outputToConsole("new ip: " + r["ip"])
                newDSTList.append(r["ip"])
                runningDSTList.append(r["ip"])


def postIt(ip, params):
    url = f"http://{ip}/api/v1/api.php"
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
    poeData = getPoeLog()

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
        'log': ",".join(str(pD) for pD in poeData)
    }

    if DEBUG:
      print(params)

    # post to self automatically
    postIt("localhost", params)

    # post to solarprotocol.net
    postIt("solarprotocol.net", params)

    for ip in ips:
        if DEBUG:
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

def runClientPostIP():
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
    url = f"http://{localHostname}/api/v1/opendata.php"
    myTZ = requests.get(url, params={'systemInfo': 'tz'}).text

    ips = getKeys("ip")
    remoteHostname = myIP if myPort == "" else f"{myIP}:{myPort}"

    apiKey = getApiKey()
    makePosts(ips, apiKey, remoteHostname, myName, myMAC, myTZ)

def outputToConsole(printThis):
    if consoleOutput:
        print(printThis)

if __name__ == "__main__":
    runClientPostIP()
else:
    consoleOutput = False
