import csv
import json
import os
import sys

from datetime import date
from enum import Enum
from typing import Union

from fastapi import FastAPI

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

class CCValue(str, Enum):
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


class SIValue(str, Enum):
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
    return os.environ['TZ'] if "TZ" in os.environ else "America/New_Yorks"

def getWattageScale():
    pvWatts = getLocal("pvWatts")
    if pvWatts != None and pvWatts != "":
        return 50.0 / float(pvWatts)

    return 1

def getLocal(key: Union[str, None]):
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

@app.get("/api/system-info")
def systemInfoValue(value: Union[SIValue, None] = None):
    match value:
        case SIValue.tz:
            return getTimezone()
        case _:
            return getLocal(value)

@app.get("/api/charge-controller")
def read_value(value: Union[CCValue, None] = None):
    filename = f"/data/traces/{date.today()}.csv"

    rows = []

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
        for row in reader:
            rows.append(row)

    if value == None:
        return row

    if value == "scaled wattage":
        return row[CCValue.PV_Power_L] * getWattageScale()

    return row[value]

    # return rows
    # print(csv, file=sys.stderr)
    # return ["assassin", "cleric", "druid", "fighter", "illusionist",
    #        "magic_user", "thief", "paladin", "ranger"]

    # line = read_csv()
    # print(line[-1])
