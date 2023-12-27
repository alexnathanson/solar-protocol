# jinja reference: https://jinja.palletsprojects.com/en/3.0.x/templates/

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import datetime
import requests
import json
import csv
import os
import re
import shutil
import sys

from typing import Optional, Union

from logging import info, debug, error, exception

from ...common.secrets import getSecret, SecretKey
from ...common.sample import fieldnames

os.chdir(sys.path[0])  # if this script is called from a different directory

serverNames = []
days = 3


# Call API for every IP address and get charge controller data
def getCC(host: str, key: str):
    info(f"GET {host} {key}")
    try:
        url = f"http://{host}/api/charge-controller"
        params = {"key": key, "days": days}
        response = requests.get(url=url, params=params, timeout=5)
        return json.loads(response.text)
    except requests.exceptions.HTTPError:
        exception(f"Http Error")
    except requests.exceptions.ConnectionError:
        exception(f"ConnectionError to {host}")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


# gets power data from charge controller
def read_csv():
    today = str(datetime.date.today())
    chargeControllerData = f"data/charge-controller/{today}.csv"
    filename = chargeControllerData

    with open(filename, "r") as data:
        reader = csv.DictReader(
            data, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames
        )
        alllines = [line for line in reader]

    line = alllines[-1]

    return line


def render_pages(_local_data, _data, _weather, _server_data):
    templatePath = f"src/protocol/build/templates"
    outputPath = f"frontend"
    host = "127.0.0.1:11215"

    pages = [
        "index.html",
        "network.html",
        "call.html",
        "documentation.html",
        "solar-web.html",
        "manifesto.html",
        "library.html",
        "guides.html",
        "site-guide.html",
    ]

    # get the current time
    time = datetime.datetime.now()
    time = time.strftime("%I:%M %p")

    # get the timezone
    try:
        url = f"http://{host}/api/system"
        response = requests.get(url=url, params={"key": "tz"})

        # for whatever reason, 404 errors weren't causing exceptions on Windows devices so this was added
        if response.status_code == 404:
            error("TZ 404 error")
            zone = "TZ n/a"
        else:
            zone = response.text

        zone = zone.replace("/", ", ").replace("_", " ")
        debug(f"{zone=}")
    except Exception:
        exception("Timezone Exception - TZ n/a")
        zone = "TZ n/a"

    # would be nice to swap this out if the via script fails
    leadImage = "images/clock.png"

    # determine mode
    if (_data["battery percentage"] * 100) > 30:
        mode = "High res mode"
    else:
        mode = "Low res mode"

    # loop through all page templates and render them with new data
    for page in pages:
        template_filename = f"{templatePath}/{page}.jinja"
        output_filename = f"{outputPath}/{page}"

        template_file = open(template_filename).read()
        info(f"rendering {template_filename}")

        # this line was changed last, it was: "/templates/"
        template = Environment(loader=FileSystemLoader(templatePath)).from_string(
            template_file
        )

        try:
            rendered_html = template.render(
                time=time,
                solarVoltage=_data["PV voltage"],
                solarCurrent=_data["PV current"],
                solarPowerL=_data["PV power L"],
                solarPowerH=_data["PV power H"],
                batteryVoltage=_data["battery voltage"],
                batteryPercentage=round(_data["battery percentage"] * 100, 1),
                batteryCurrent=_data["battery current"],
                loadVoltage=_data["load voltage"],
                loadCurrent=_data["load current"],
                loadPower=_data["load power"],
                name=_local_data["name"],
                description=_local_data["description"],
                location=_local_data["location"],
                city=_local_data["city"],
                country=_local_data["country"],
                lat=_local_data["lat"],
                lon=_local_data["lon"],
                bgColor=_local_data["bgColor"],
                font=_local_data["font"],
                weather=_weather["description"],
                temp=_weather["temp"],
                feelsLike=_weather["feels_like"],
                sunrise=_weather["sunrise"],
                sunset=_weather["sunset"],
                zone=zone,
                leadImage=leadImage,
                mode=mode,
                servers=_server_data,
            )
        except:
            rendered_html = template.render(
                time=time,
                solarVoltage="n/a",
                solarCurrent="n/a",
                solarPowerL="n/a",
                solarPowerH="n/a",
                batteryVoltage="n/a",
                batteryPercentage=50,
                batteryCurrent="n/a",
                loadVoltage="n/a",
                loadCurrent="n/a",
                loadPower="n/a",
                name=_local_data["name"],
                description=_local_data["description"],
                location=_local_data["location"],
                city=_local_data["city"],
                country=_local_data["country"],
                lat=_local_data["lat"],
                long=_local_data["long"],
                bgColor=_local_data["bgColor"],
                font=_local_data["font"],
                weather=_weather["description"],
                temp=_weather["temp"],
                feelsLike=_weather["feels_like"],
                sunrise=_weather["sunrise"],
                sunset=_weather["sunset"],
                zone=zone,
                leadImage=leadImage,
                mode=mode,
                servers=_server_data,
                dev="",
            )

        open(output_filename, "w").write(rendered_html)


# get weather data
def get_weather(lon, lat, appid: str):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"lon": lon, "lat": lat, "appid": appid}
    debug(f"{params=}")

    response = requests.get(url=url, params=params)
    response.raise_for_status()

    data = response.json()
    current_temperature = data["main"]["temp"]
    current_humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")

    output = {
        "description": data["weather"][0]["description"],
        "temp": round(data["main"]["temp"] - 273.15, 1),
        "feels_like": round(data["main"]["feels_like"] - 273.15, 1),
        "sunrise": sunrise,
        "sunset": sunset,
    }

    debug(f"{output=}")

    return output


def getLocal():
    filename = f"local/local.json"
    with open(filename) as localfile:
        return json.load(localfile)


def getDeviceInfo(key: str) -> list[Optional[Union[str, list[str]]]]:
    devices = f"data/devices.json"
    try:
        with open(devices) as file:
            data = json.load(file)
    except FileNotFoundError:
        with open(devices, "w") as file:
            json.dump([], file)
            data = []

    default = [] if key == "log" else None
    return [device.get(key) for device in data]


def get_ips():
    ips = getDeviceInfo("ip")
    httpPorts = getDeviceInfo("httpPort")
    hosts = [ str.join(':', (ip, httpPort)) for ip, httpPort in zip(ips, httpPorts) ]
    serverNames = getDeviceInfo("name")

    devices = dict(zip(serverNames, hosts))
    debug(f"{devices=}")
    return devices


# Call API for every IP address and get charge controller data
def get_pv_value(ip):
    try:
        response = requests.get(
            f"http://{ip}/api/charge-controller",
            params={"value": "PV-voltage"},
            timeout=5,
        )
        if response.status_code == 200:
            [latest] = response.json()
            return latest["PV voltage"]
    except requests.exceptions.HTTPError:
        error(f"Http Error")
    except requests.exceptions.ConnectionError:
        error(f"Connection Error")
    except requests.exceptions.Timeout:
        error(f"Timeout")
    except requests.exceptions.RequestException:
        error(f"Request Error")


# return data from a particular server
def getSystem(ip):
    try:
        # returns a single value
        response = requests.get(f"http://{ip}/api/system", timeout=5)
        return response.json()
    except requests.exceptions.HTTPError:
        exception(f"HTTP Error")
    except requests.exceptions.ConnectionError:
        exception(f"Connection Error")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


def download_file(url, local_filename=None):
    return local_filename


def getFormattedTimestampFor(itemNumber):
    try:
        timestamps = getDeviceInfo("timestamp")
        timestamp = timestamps[itemNumber]
        debug(f"{timestamp=}")

        formattedTimestamp = datetime.datetime.fromtimestamp(timestamp).strftime(
            "%m/%d/%Y %H:%M:%S"
        )
        debug(f"{formattedTimestamp=}")
        return formattedTimestamp

    except Exception:
        return "N/A"


def makeLinkFor(name: str, status: str, ip: str):
    # make lower case, remove spaces, remove nonstandard characters
    lowercaseNospace = name.lower().replace(" ", "")
    sanitizedName = re.sub("[^A-Za-z0-9-_]+", "", lowercaseNospace)
    serverURL = f"http://{ip}/network/{sanitizedName}"
    if status == "offline":
        return serverURL

    return f"<a href='{serverURL}'>{serverURL}</a>"


def getServerDataFor(name: str, ip: str):
    # FIXME: reformat page so offline servers dont actually need this blank data
    default = {
        "ip": ip,
        "name": name,
        "description": "",
        "city": "",
        "location": "",
        "country": "",
    }

    try:
        system = getSystem(ip)
        if system == None:
            return default
        else:
            system["ip"] = ip
            return system

    except Exception:
        exception("issue getting system info")
        return default


def getLocalWeatherFor(lon, lat):
    appid = getSecret(SecretKey.appid)
    try:
        local_weather = get_weather(lon=lon, lat=lat, appid=appid)
        return local_weather
    except Exception as exception:
        info(exception)
        return {
            "description": "n/a",
            "temp": "n/a",
            "feels_like": "n/a",
            "sunrise": "n/a",
            "sunset": "n/a",
        }


def main():
    info("***** Running html.py *****")

    # 1. get IP list of addresses
    deviceList_data = get_ips()

    # 2 Collect data from all the difference servers on the network
    server_data = [
        getServerDataFor(name=name, ip=ip) for name, ip in deviceList_data.items()
    ]

    # 3. get solar data and add it to server_data
    for itemNumber, item in enumerate(server_data):
        item["solar_voltage"] = get_pv_value(item["ip"])
        item["status"] = "offline" if item["solar_voltage"] == None else "online"
        item["timestamp"] = getFormattedTimestampFor(itemNumber)
        item["link"] = makeLinkFor(item["name"], item["status"], item["ip"])

    # 4. get images and render pages
    local_data = getLocal()
    energy_data = read_csv()  # get pv data from local csv
    local_weather = getLocalWeatherFor(local_data["lon"], local_data["lat"])

    render_pages(local_data, energy_data, local_weather, server_data)


if __name__ == "__main__":
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")

    main()
