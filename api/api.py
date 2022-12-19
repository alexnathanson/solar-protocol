import csv
import datetime
import json
import os
import sys

from enum import Enum
from typing import Union

from fastapi import FastAPI, Header, Form
from solar_secrets import getSecret, setSecret, SecretKey
from solar_common import fieldnames
import requests

# safelist of keys we can share from local.json
safe_keys = [
    "color",
    "name",
    "description",
    "location",
    "city",
    "country",
    "pvWatts",
    "pvVolts",
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
    return os.environ.get("TZ", "America/New_York")


def getWattageScale():
    pvWatts = getLocal("pvWatts")
    if pvWatts != None and pvWatts != "":
        return 50.0 / float(pvWatts)

    return 1


@app.get("/api")
def root():
    return {"message": "Hello World 👋"}


class DeviceKeys(str, Enum):
    tz = "tz"
    name = "name"
    log = "log"
    timestamp = "timestamp"
    ip = "ip"
    httpPort = "httpPort"


@app.get("/api/status")
def status():
    response = requests("/status")
    status = response.text.split("\n")
    stats = status[2]
    [accepts, handled, reqs] = status.split(" ")

    return {
        "uptime": "todo",
        "rps": "todo",
        "accepts": accepts,
        "handled": handled,
        "requests": reqs,
        "cpu load": "todo",
    }


@app.post("/api/device")
def updateDevice(
    tz: Union[str, None] = Form(),
    mac: Union[str, None] = Form(),
    name: Union[str, None] = Form(),
    log: Union[str, None] = Form(),
    ip: Union[str, None] = Form(),
    httpPort: Union[str, None] = Form(),
    timestamp: Union[float, None] = Form(),
    apiKey: str = Form(),
):

    if apiKey != getSecret(SecretKey.apiKey):
        raise Error("Invalid apiKey for this server")

    formData = {
        "tz": tz,
        "mac": mac,
        "name": name,
        "log": log,
        "ip": ip,
        "httpPort": httpPort,
        "timestamp": timestamp,
    }
    postedDevice = {key: value for (key, value) in formData.items() if value}

    filename = f"/data/devices.json"

    with open(filename, "r") as devicesfile:
        devices = json.load(devicesfile)

    # update the device if we already found its mac...
    foundDevice = None
    for device in devices:
        if device.get("mac") == mac:
            device.update(postedDevice)
            foundDevice = device

    # otherwise, add it to the list
    if foundDevice is None:
        devices.append(postedDevice)

    with open(filename, "w") as devicesfile:
        json.dump(devices, devicesfile)

    with open(filename, "r") as devicesfile:
        for device in json.load(devicesfile):
            if device.get("mac") == mac:
                return device


@app.get("/api/devices")
def devices(key: Union[DeviceKeys, None] = None):
    filename = f"/data/devices.json"

    with open(filename, "r") as jsonfile:
        devices = json.load(jsonfile)

    if key == None:
        return [{key: device.get(key) for key in DeviceKeys} for device in devices]

    return [{key: device.get(key)} for device in devices]


@app.get("/api/system")
def system(key: Union[SystemKeys, None] = None):
    if key == SystemKeys.tz:
        return getTimezone()

    return getLocal(key)


@app.get("/api/charge-controller/{day}")
def getChargeForDay(day: str, key: Union[ChargeKeys, None] = None):
    return charge(days=[day], key=key)


@app.get("/api/charge-controller")
def getCharge(days: Union[int, None] = None, key: Union[ChargeKeys, None] = None):
    today = datetime.date.today()

    if days == None:
        return charge(days, key=key)

    return charge(
        days=[today - datetime.timedelta(days=days) for days in range(days)], key=key
    )


def charge(days: Union[list[str], None] = None, key: Union[ChargeKeys, None] = None):
    filepath = "/data/traces"

    rows = []
    if days == None:
        dates = [datetime.date.today()]
    else:
        dates = days

    for date in dates:
        try:
            with open(f"{filepath}/{date}.csv", "r") as csvfile:
                reader = csv.DictReader(
                    csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames
                )
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            continue  # its okay if we are missing data

    # only show most recent chage if no days passed
    if days == None:
        rows = [rows[-1]]

    # enrich with the scaled wattage
    wattageScale = getWattageScale()
    dataWithWattage = [
        row | {"scaled wattage": row[ChargeKeys.PV_power_L] * wattageScale}
        for row in rows
    ]

    # then filter on key
    if key != None:
        return [
            {key: row[key], "timestamp": row["timestamp"]} for row in dataWithWattage
        ]

    return dataWithWattage


# X-Real-Ip is set in the nginx config
@app.get("/api/myip")
def getChargeForDay(x_real_ip: str | None = Header(default=None)):
    return x_real_ip


def getDNSKey():
    filename = f"/data/dnskey.txt"

    with open(filename, "r") as dnskeyfile:
        return readline()


@app.get("/api/blocklist")
def blocklist():
    with open("/data/blocklist.json") as blocklistfile:
        return json.load(blocklistfile)


def updatePoeLog(name: str, ip: str):
    fileName = f"/data/dns.log"

    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[name, ip])
        writer.writerow([name, ip])


@app.post("/api/profile")
def updateProfileImage(profile: str):
    fileName = f"/local/serverprofile.gif"

    with open(fileName, "w") as profilefile:
        write(profile, profilefile)


@app.get("/api/local")
def getLocal(key: Union[SystemKeys, None]):
    filename = f"/local/local.json"

    with open(filename, "r") as jsonfile:
        localData = json.load(jsonfile)

    if key == None:
        safe_data = {key: getLocal(key) for key in safe_keys}
        safe_data["timezone"] = getTimezone()
        safe_data["wattage-scale"] = getWattageScale()
        return safe_data

    if key == "color":
        return localData.get("bgColor")

    # FIXME: SECURITY: Can ask for 'unsafe' keys here
    return localData.get(key)


@app.post("/api/local")
def updateLocal(
    name: Union[str, None] = Form(),
    description: Union[str, None] = Form(),
    location: Union[str, None] = Form(),
    city: Union[str, None] = Form(),
    country: Union[str, None] = Form(),
    lat: Union[str, None] = Form(),
    lon: Union[str, None] = Form(),
    pvWatts: Union[str, None] = Form(),
    pvVolts: Union[str, None] = Form(),
    httpPort: Union[str, None] = Form(),
):
    formData = {
        "name": name,
        "description": description,
        "location": location,
        "city": city,
        "country": country,
        "lat": lat,
        "lon": lon,
        "pvWatts": pvWatts,
        "pvVolts": pvVolts,
        "httpPort": httpPort,
    }

    # filter out empty or none
    filtered = {key: value for (key, value) in formData.items() if value}

    filename = f"/local/local.json"
    with open(filename, "r") as localfile:
        local = json.load(localfile)

    local.update(filtered)

    with open(filename, "w") as localfile:
        json.dump(local, localfile)

    return local


@app.post("/api/secret")
def setEnv(key: SecretKey, value: str):
    if not isHash(value):
        raise Error(f"Secret value for `{key}` not a valid hash")

    if value == hash(""):
        raise Error(f"Secret value for `{key}` is empty, will not continue")

    if value in top_500_password_hashes:
        raise Error(
            f"Secret value for `{key}` is in top 500 passwords, please choose another"
        )

    return setSecret(key, value)
