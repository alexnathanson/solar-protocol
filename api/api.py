import csv
import datetime
import json
import os
import sys

from enum import Enum
from typing import Union

from fastapi import FastAPI, Header

import requests

# header for datalogger csv
fieldnames = [
    "timestamp",
    "PV voltage",
    "PV current",
    "PV power L",
    "PV power H",
    "battery voltage",
    "battery current",
    "battery power L",
    "battery power H",
    "load voltage",
    "load current",
    "load power",
    "battery percentage",
]

# safelist of keys we can share from local.json
safe_keys = [
    "color",
    "name",
    "description",
    "location",
    "city",
    "country",
    "pvWatts",
    "pvVolts"
]

class ChargeKeys(str, Enum):
    PV_voltage = "PV voltage"
    PV_current = "PV current"
    PV_power_L = "PV power L"
    PV_power_H = "PV power H"
    battery_voltage = "battery voltage"
    battery_current = "battery current"
    battery_power_L = "battery power L"
    battery_power_H = "battery power H"
    load_voltage = "load voltage"
    load_current = "load current"
    load_power = "load power"
    battery_percentage = "battery percentage"
    scaled_wattage = "scaled wattage"


class SystemKeys(str, Enum):
    tz = "tz"
    color = "color"
    description = "description"
    name = "name"
    location = "location"
    city = "city"
    country = "country"
    pvWatts = "pvWatts"
    pvVolts = "pvVolts"


app = FastAPI(title="solar-protocol", docs_url="/api/docs")

def getTimezone():
    return os.environ['TZ'] if "TZ" in os.environ else "America/New_York"

def getWattageScale():
    pvWatts = getLocal("pvWatts")
    if pvWatts != None and pvWatts != "":
        return 50.0 / float(pvWatts)

    return 1

def getLocal(key: Union[SystemKeys, None]):
    filename = f"/local/local.json"

    with open(filename, "r") as jsonfile:
        localData = json.load(jsonfile)

    if key == None:
        safe_data = { key: getLocal(key) for key in safe_keys }
        safe_data["timezone"] = getTimezone()
        safe_data["wattage-scale"] = getWattageScale()
        return safe_data
        
    if key == "color":
        return localData["bgColor"]

    return localData[key]

@app.get("/api")
def root():
    return {"message": "Hello World 👋"}

class DeviceKeys(str, Enum):
    tz = "tz"
    name = "name"
    log = "log"
    timestamp = "timestamp"

@app.get("/api/status")
def devices():
    response = requests("/status")
    status = response.text.split("\n")
    stats = status[2]
    [accepts, handled, reqs] = status.split(' ')

    return {
            "uptime": "todo",
            "rps": "todo",
            "accepts": accepts,
            "handled": handled,
            "requests": reqs,
            "cpu load": "todo",
    }

@app.get("/api/devices")
def devices(key: Union[DeviceKeys, None] = None):
    filename = f"/data/devices.json"

    with open(filename, "r") as jsonfile:
        devices = json.load(jsonfile)

    if key == None:
        return [{ key: device[key] for key in DeviceKeys } for device in devices]

    return [{ key: device[key] } for device in devices]


@app.get("/api/system")
def system(key: Union[SystemKeys, None] = None):
    if key == SystemKeys.tz:
        return getTimezone()

    return getLocal(key)

@app.get("/api/charge/{day}")
def getChargeForDay(day: str, key: Union[ChargeKeys, None] = None):
    return charge(days=[day], key=key)

@app.get("/api/charge")
def getCharge(days: Union[int, None] = None, key: Union[ChargeKeys, None] = None):
    today = datetime.date.today()

    if days == None:
        return charge(days, key=key)

    return charge(days=[ today - datetime.timedelta(days=days) for days in range(days)], key=key)

def charge(days: Union[list[str], None] = None, key: Union[ChargeKeys, None] = None):
    filepath = "/data/traces"

    rows = []
    if days == None:
        dates = [ datetime.date.today() ]
    else:
        dates = days

    for date in dates:
        try:
            with open(f"{filepath}/{date}.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            continue # its okay if we are missing data

    # only show most recent chage if no days passed
    if days == None:
        rows = [ rows[-1] ]

    # enrich with the scaled wattage
    wattageScale = getWattageScale()
    dataWithWattage = [ row | { "scaled wattage": row[ChargeKeys.PV_power_L] * wattageScale } for row in rows ]

    # then filter on key
    if key != None:
        return [ { key: row[key], "timestamp": row["timestamp"] } for row in dataWithWattage ]

    return dataWithWattage

# X-Real-Ip is set in the nginx config
@app.get("/api/myip")
def getChargeForDay(x_real_ip: str | None = Header(default=None))
    return x_real_ip

def getDNSKey():
    filename = f"/data/dnskey.txt"

    with open(filename, "r") as dnskeyfile:
        return readline()

@app.get("/api/allowlist")
def allowlist():
    # TODO: swtich to file
    return {
        "Hells Gate": "$2y$10$5/O1zeTvLmxBNIRpmqve5u6x9RmL8JBi./dzgD3mwfudHEBuABFQ6",
        "Chile": "$2y$10$M3RtM5fYwzUXYQJRx1OGDe9oPSAmnApDPlCWpYCpHXcQixCPVaNge",
        "Caddie": "$2y$10$157Qs27b4.gUAHlF0o/i5ufIF/tclJ8GitcIQbgeA9t76XYF0S0Ve",
        "Low_Carbon_Methods": "$2y$10$2vFdQ05rQyGFIbY6WjncE.nZgimUEfIoCQKoQmK1qNLSPfc3T2NXy",
        "Dominica": "$2y$10$MLdkxh3qzwwU0yucGTBte.964aMIPxRHa4UiH3o0AH67jGk5P5nDu",
        "Kenya": "$2y$10$3EuwWV0KuoBhBBJd3Q7uX.2XHNIYZZkn0mpUjXSLHd6vGFlAXhyGe",
        "Fiber_Fest": "$2y$10$42gKyu4kJeMnbOn79hJyQOBxE3aqV1OCXSwaWasg1Dvi0goII2fKK",
        "Swarthmore ": "$2y$10$43RlEFdYJqqc5Odvnr.ol.pbJ0A.p7td3rIzz4Z3V56KpQ0cLogJe"
    }

@app.get("/api/blocklist")
def blocklist():
    # TODO: switch to file
    # TODO: extend to support multiple burned keys from the same server
    return {
        "Tega": "",
        "SPfA": "$2y$10$8jr3efgV3/N2RosUY0cH1edYXYcYNE4Iwi6RHqYwyupnccYVX9f5.",
        "Beijing": "$2y$10$0uZh7HjT27KTN5uszOCuxe6yhEWbWxzX/i/ZY1vIfZg1xqfNgshmS"
    }

@app.post("/api/ip")
def updateDNS(key: str, ip: str):
    name = verifyPasswordAndReturnName(key)

    params = {
        host: '@',
        domain: 'solarprotocol.net',
        password: key,
        ip: ip
    }

    response = request.get("https://dynamicdns.park-your-domain.com/update", params=params)
    if response.status == 200:
        updatePoeLog(name, ip)

def verifyPasswordAndReturnName(key: str):
    for name, hash in allowList():
        if key == hash:
            return name

    raise Exception('Incorrect password')

def updatePoeLog(name: str, ip: str):
    fileName = f"/data/dns.log"

    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[name, ip])
        writer.writerow([name, ip])
