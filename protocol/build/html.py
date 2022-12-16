# jinja reference: https://jinja.palletsprojects.com/en/3.0.x/templates/

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import datetime
import requests
import json
import csv
import os
import re
import sys

from logging import info, debug, error, exception

from solar_secrets import getSecret, SecretKey
from solar_common import fieldnames

os.chdir(sys.path[0])  # if this script is called from a different directory

serverNames = []
days = 3


# Call API for every IP address and get charge controller data
def getCC(server, key):
    info(f"GET {server} {key}")
    try:
        url = f"http://{server}/api/charge-controller"
        params = {"key": key, "days": days}
        response = requests.get(url=url, params=params, timeout=5)
        return json.loads(response.text)
    except requests.exceptions.HTTPError:
        exception(f"Http Error")
    except requests.exceptions.ConnectionError:
        exception(f"ConnectionError to {server}")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


# gets power data from charge controller
def read_csv():
    today = str(datetime.date.today())
    chargeControllerData = f"/data/traces/{today}.csv"
    filename = chargeControllerData

    with open(filename, "r") as data:
        reader = csv.DictReader(
            data, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames
        )
        alllines = [line for line in reader]

    line = alllines[-1]

    return line


def render_pages(_local_data, _data, _weather, _server_data):
    debug(_data)
    debug(_local_data)

    templatePath = f"/protocol/build/templates"
    outputPath = f"/frontend"

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
        ip = _server_data["ip"]
        url = f"http://{ip}/api/system"
        response = requests.get(url=url, params={"key": "tz"})

        # for whatever reason, 404 errors weren't causing exceptions on Windows devices so this was added
        if response.status == 404:
            error("TZ 404 error")
            zone = "TZ n/a"
        else:
            zone = response.text

        zone = zone.replace("/", " ")
        info(f"ZONE {zone}")
    except Exception as e:
        error("Timezone Exception - TZ n/a")
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
def get_weather(lon, lat, appid):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"lon": lon, "lat": lat, "appid": appid}

    response = requests.get(url=url, params=params)
    data = response.json()
    current_temperature = data["main"]["temp"]
    current_humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")

    info(" Temperature (in kelvin unit) = {current_temperature}")
    info(" humidity (in percentage) = {current_humidity}")
    info(" description = {weather_description}")

    output = {
        "description": data["weather"][0]["description"],
        "temp": round(data["main"]["temp"] - 273.15, 1),
        "feels_like": round(data["main"]["feels_like"] - 273.15, 1),
        "sunrise": sunrise,
        "sunset": sunset,
    }

    return output


# get local front end data
def get_local():
    filename = f"/local/local.json"
    with open(filename) as localfile:
        return json.load(localfile)


# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []
    devices = f"/data/devices.json"

    with open(devices) as f:
        data = json.load(f)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList


def get_ips():
    ips = getDeviceInfo("ip")
    serverNames = getDeviceInfo("name")

    devices = dict(zip(serverNames, ips))
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
    # Downloads a file from a remote URL
    if local_filename is None:
        local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def check_images(server_data):
    for server in server_data:
        filename = server["name"] + ".gif"
        filename = filename.replace(" ", "-")
        fullpath = "/frontend/images/servers/{filename}"
        filepath = "images/servers/{filename}"

        if "ip" in server:
            ip = server["ip"]
            name = server["name"]
            debug(f"server {name}: {ip}")

            if ip == "api":  # if it is itself
                info("*** LOCAL HOST ***")
                # TODO: make this work with irregular ports
                image_path = imgDst
                filepath = image_path
            elif os.path.exists(fullpath):  # else if the image is in the folder
                info(f"Got image for {name}")
            else:
                # else download image using api and save it to the folder: "../../frontend/images/servers/"
                image_path = f"http://{ip}/serverprofile.gif"
                try:
                    download_file(image_path, fullpath)
                    debug(image_path)
                    debug(local_path)
                except Exception as e:
                    error(f"{name}: Offline. Can't get image")
            server["image_path"] = filepath


def getFormattedTimestampFor(itemNumber):
    try:
        timestamps = getDeviceInfo("timestamp")
        timestamp = timestamps[itemNumber]
        debug(timestamp)

        formattedTimestamp = datetime.datetime.fromtimestamp(timestamp).strftime(
            "%m/%d/%Y %H:%M:%S"
        )
        debug(formattedTimestamp)
        return formattedTimestamp

    except Exception:
        return "N/A"


def makeLinkFor(name: str, status: str):
    # make lower case, remove spaces, remove nonstandard characters
    lowercaseNospace = name.lower().replace(" ", "")
    sanitizedName = re.sub("[^A-Za-z0-9-_]+", "", lowercaseNospace)
    serverURL = f"http://solarprotocol.net/network/{sanitizedName}"
    if status == "offline":
        return serverURL

    return f"<a href='{serverURL}'>{serverURL}</a>"


def getServerDataFor(name: str, ip: str):
    try:
        [system] = getSystem(ip)
        debug(system)
        system["ip"] = ip
        return system

    except Exception as exception:
        error(exception)

        # FIXME: reformat page so offline servers dont actually need this blank data
        return {
            "ip": ip,
            "name": name,
            "description": "",
            "city": "",
            "location": "",
            "country": "",
        }


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
    debug(deviceList_data)

    # 2 Collect data from all the difference servers on the network
    server_data = [
        getServerDataFor(name=name, ip=ip) for name, ip in deviceList_data.items()
    ]

    # 3. get solar data and add it to server_data
    for itemNumber, item in enumerate(server_data):
        item["solar_voltage"] = get_pv_value(item["ip"])
        item["status"] = "offline" if item["solar_voltage"] == None else "online"
        item["timestamp"] = getFormattedTimestampFor(itemNumber)
        item["link"] = makeLinkFor(item["name"], item["status"])

    # 4. get images and render pages
    debug(server_data)
    local_data = get_local()
    debug(local_data)
    check_images(server_data)
    energy_data = read_csv()  # get pv data from local csv
    debug(energy_data)
    local_weather = getLocalWeatherFor(local_data["lon"], local_data["lat"])

    render_pages(local_data, energy_data, local_weather, server_data)


if __name__ == "__main__":
    main()
