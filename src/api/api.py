import uvicorn
import csv
import datetime
import json
import os

from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Form, Request
from passlib.hash import bcrypt
from ..common.secrets import getSecret, setSecret, SecretKey
from ..common.sample import fieldnames
from logging import error
import requests

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

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
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def getTimezone():
    return os.environ.get("TZ", "America/New_York")


def getWattageScale():
    pvWatts = getLocal("pvWatts")
    if pvWatts is not None and pvWatts != "":
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
    status[2]
    [accepts, handled, reqs] = status.split(" ")

    return {
        "uptime": "todo",
        "rps": "todo",
        "accepts": accepts,
        "handled": handled,
        "requests": reqs,
        "cpu load": "todo",
    }


def allowlist():
    with open("data/allowlist.json", "r") as allowlistfile:
        return json.load(allowlistfile)


def updateDnsLog(name: str, ip: str, timestamp):
    with open("data/dns.log", "a+", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[name, ip, timestamp])
        writer.writerow([name, ip, timestamp])


@app.post("/api/limit")
@limiter.limit("5/minute")
def limit(request: Request, key: str = Form()):
    ip = get_remote_address(request)
    return f"{ip=} {key=}"


@app.post("/api/update")
@limiter.limit("5/minute")
def updateDNS(request: Request, key: str = Form()):
    ip = get_remote_address(request)

    if len(key) != 16:
        raise HTTPException(status_code=403)

    for name, password_hash in allowlist().items():
        if bcrypt.verify(key, password_hash):
            host = "beta"
            domain = "solarprotocol.net"
            password = getSecret(SecretKey.dnspassword)

            params = {host, domain, ip, password}
            url = "https://dynamicdns.park-your-domain.com/update"

            response = request.get(url=url, params=params)

            if response.status_code == 200:
                timestamp = datetime.datetime.now()
                updateDnsLog(name, ip, timestamp)
                return f"beta.solarprotocol.net: {ip=}"
            else:
                error(response.text)
                raise HTTPException("issue updating dns")

    raise HTTPException(status_code=403)


# This is a list of announced devices.
@app.post("/api/device")
def updateDevice(
    tz: Optional[str] = Form(),
    mac: Optional[str] = Form(),
    name: Optional[str] = Form(),
    log: Optional[list[Optional[str]]] = Form([]),
    ip: Optional[str] = Form(),
    httpPort: Optional[str] = Form(),
    timestamp: Optional[float] = Form(),
    networkkey: str = Form(),
):
    if networkkey is None:
        raise Exception("Invalid networkkey for this server")

    if networkkey != getSecret(SecretKey.networkkey):
        raise Exception("Invalid networkkey for this server")

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

    devicesFilename = "data/devices.json"

    try:
        with open(devicesFilename, "r") as devicesfile:
            devices = json.load(devicesfile)
    except FileNotFoundError:
        with open(devicesFilename, "w") as jsonfile:
            json.dump([], jsonfile)
            devices = []

    # update the device if we already found its mac...
    foundDevice = None
    for device in devices:
        if device.get("mac") == mac:
            device.update(postedDevice)
            foundDevice = device

    # otherwise, add it to the list
    if foundDevice is None:
        devices.append(postedDevice)

    with open(devicesFilename, "w") as devicesfile:
        json.dump(devices, devicesfile)

    with open(devicesFilename, "r") as devicesfile:
        for device in json.load(devicesfile):
            if device.get("mac") == mac:
                return device


@app.get("/api/devices")
def devices(key: Optional[DeviceKeys] = None):
    filename = "data/devices.json"
    try:
        with open(filename, "r") as jsonfile:
            devices = json.load(jsonfile)
        if key is None:
            return [{key: device.get(key) for key in DeviceKeys} for device in devices]

        return [{key: device.get(key)} for device in devices]
    except FileNotFoundError:
        with open(filename, "w") as jsonfile:
            json.dump([], jsonfile)
            return []


@app.get("/api/system")
def system(key: Optional[SystemKeys] = None):
    if key == SystemKeys.tz:
        return getTimezone()

    return getLocal(key)


@app.get("/api/charge-controller/{day}")
def getChargeForDay(day: str, key: Optional[ChargeKeys] = None):
    return charge(days=[day], key=key)


@app.get("/api/charge-controller")
def getCharge(days: Optional[int] = None, key: Optional[ChargeKeys] = None):
    today = datetime.date.today()

    if days is None:
        return charge(days, key=key)

    return charge(
        days=[today - datetime.timedelta(days=days) for days in range(days)], key=key
    )


def charge(days: Optional[list[str]] = None, key: Optional[ChargeKeys] = None):
    rows = []
    if days is None:
        dates = [datetime.date.today()]
    else:
        dates = days

    for date in dates:
        try:
            with open(f"data/charge-controller/{date}.csv", "r") as csvfile:
                reader = csv.DictReader(
                    csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames
                )
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            continue  # its okay if we are missing data

    # only show most recent chage if no days passed
    if days is None:
        rows = [rows[-1]]

    # enrich with the scaled wattage
    wattageScale = getWattageScale()
    dataWithWattage = [
        row | {"scaled wattage": row[ChargeKeys.PV_power_L] * wattageScale}
        for row in rows
    ]

    # then filter on key
    if key is not None:
        return [
            {key: row[key], "timestamp": row["timestamp"]} for row in dataWithWattage
        ]

    return dataWithWattage


# X-Real-Ip is set in the nginx config
@app.get("/api/myip")
def getMyIp(x_real_ip: str | None = Header(default=None)):
    return x_real_ip


@app.post("/api/profile")
def updateProfileImage(profile: str):
    raise Exception("Unimplemented")
    # FIXME: Protect this route
    with open("local/serverprofile.gif", "w") as profilefile:
        profilefile.write(profile)


@app.get("/api/local")
def getLocal(key: Optional[SystemKeys]):
    with open("local/local.json", "r") as jsonfile:
        localData = json.load(jsonfile)

    if key is None:
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
    name: Optional[str] = Form(),
    description: Optional[str] = Form(),
    location: Optional[str] = Form(),
    city: Optional[str] = Form(),
    country: Optional[str] = Form(),
    lat: Optional[str] = Form(),
    lon: Optional[str] = Form(),
    pvWatts: Optional[str] = Form(),
    pvVolts: Optional[str] = Form(),
    httpPort: Optional[str] = Form(),
):
    raise Exception("Unimplemented")
    # FIXME: Protect this route
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

    filename = "local/local.json"
    with open(filename, "r") as localfile:
        local = json.load(localfile)

    local.update(filtered)

    with open(filename, "w") as localfile:
        json.dump(local, localfile)

    return local


# FIXME: Protect this route
@app.post("/api/secret")
def setEnv(key: SecretKey, value: str):
    raise Exception("Unimplemented")

    def isHash(value):
        raise Exception("fix hash check")
        return len(value) > 8

    top_500_password_hashes = ["god", "money", "sex"]

    if not isHash(value):
        raise Exception(f"Secret value for `{key}` not a valid hash")

    if value == hash(""):
        raise Exception(f"Secret value for `{key}` is empty, will not continue")

    if value in top_500_password_hashes:
        raise Exception(
            f"Secret value for `{key}` is in top 500 passwords, please choose another"
        )

    return setSecret(key, value)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11215, proxy_headers=True)
