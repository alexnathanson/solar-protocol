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

os.chdir(sys.path[0])  # if this script is called from a different directory
DEV = "DEV" in sys.argv

serverNames = []
myIP = " "
days = 3

# Call API for every IP address and get charge controller data
def getCC(server, key):
    print(f"GET {server} {key}")
    try:
        url = f"http://{server}/api/charge-controller?key={key}&days={days}"
        response = requests.get(url, timeout=5)
        return json.loads(response.text)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError:
        print(f"Timed out connecting to {server}")
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# gets power data from charge controller
def read_csv():
    today = str(datetime.date.today())
    chargeControllerData = f"/data/traces/{today}.csv"
    filename = chargeControllerData

    with open(filename, "r") as data:
        alllines = [line for line in csv.DictReader(data)]

    line = alllines[-1]
    line["PV voltage"] = float(line["PV voltage"])
    line["PV current"] = float(line["PV current"])
    line["PV power L"] = float(line["PV power L"])
    line["PV power H"] = float(line["PV power H"])
    line["battery voltage"] = float(line["battery voltage"])
    line["battery current"] = float(line["battery current"])
    line["battery power L"] = float(line["battery power L"])
    line["battery power H"] = float(line["battery power H"])
    line["load voltage"] = float(line["load voltage"])
    line["load current"] = float(line["load current"])
    line["load power"] = float(line["load power"])
    line["battery percentage"] = float(line["battery percentage"])
    return line


def render_pages(_local_data, _data, _weather, _server_data):
    print("Battery Percentage: {str(_data['battery percentage'])}")

    templatePath = f"./templates"
    outputPath = f"/frontend"

    pages = [
        "index.html",
        "network.html",
        "call.html",
        "documentation.html",
        "solar-web.html",
        "manifesto.html",
        "library.html",
    ]

    # get the current time
    time = datetime.datetime.now()
    time = time.strftime("%I:%M %p")

    # get the timezone
    try:
        tz_url = "http://localhost/api/system?key=tz"
        response = requests.get(tz_url)

        # for whatever reason, 404 errors weren't causing exceptions on Windows devices so this was added
        if response.status == 404:
            print("TZ 404 error")
            zone = "TZ n/a"
        else:
            zone = response.text

        zone = zone.replace("/", " ")
        print("ZONE", zone)
    except Exception as e:
        print("Timezone Exception - TZ n/a")
        zone = "TZ n/a"

    # print("UTC TIME", datetime.datetime.utcnow())
    # would be nice to swap this out if the via script fails
    leadImage = "images/clock.png"

    # determine mode
    if (_data["battery percentage"] * 100) > 30:
        mode = "High res mode"
    else:
        mode = "Low res mode"

    # loop through all page templates and render them with new data
    for page in pages:
        template_filename = f"{templatePath}/{filename}"
        output_filename = f"{outputPath}/{filename}"
        template_file = open(template_filename).read()
        print("rendering", template_filename)

        # this line was changed last, it was: "/templates/"
        template = Environment(loader=FileSystemLoader(templatePath)).from_string(
            template_file
        )

        # template = Template(template_file)
        rendered_html = template.render(
            time=time,
            solarVoltage=_data["PV voltage"],
            solarCurrent=_data["PV current"],
            solarPowerL=_data["PV power L"],
            solarPowerH=_data["PV power H"],
            batteryVoltage=_data["battery voltage"],
            batteryPercentage=round(_data["battery percentage"] * 100, 1),
            batterCurrent=_data["battery current"],
            loadVoltage=_data["load voltage"],
            loadCurrent=_data["load current"],
            loadPower=_data["load power"],
            name=_local_data["name"],
            # url=_local_data["url"],
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
            dev=" DEV" if DEV else "",
        )

        # print(rendered_html)
        open(output_filename, "w").write(rendered_html)


# get weather data
def get_weather(lon, lat, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}?lon={lon}&lat={lat}&appid={api_key}"
    if DEV:
        print(url)

    response = requests.get(url)
    data = response.json()
    current_temperature = data["main"]["temp"]
    current_humidiy = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")

    print(
        " Temperature (in kelvin unit) = "
        + str(current_temperature)
        + "\n humidity (in percentage) = "
        + str(current_humidiy)
        + "\n description = "
        + str(weather_description)
    )

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
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary


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
    # FIXME: should we remove the server. and be fully p2p?
    myIP = requests.get("https://server.solarpowerforartists.com/?myip").text

    ips = getDeviceInfo("ip")
    serverNames = getDeviceInfo("name")

    devices = dict(zip(serverNames, ips))
    return devices


def active_servers(dst):
    try:
        x = requests.get("http://" + dst + "/local", timeout=5)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# Call API for every IP address and get charge controller data
def get_pv_value(ip):
    try:
        response = requests.get(
            f"http://{ip}/api/charge-controller", params={"value": "PV-voltage"}, timeout=5
        )
        [latest] = response.json
        return latest.pop()["PV voltage"]
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# return data from a particular server
def getSystem(ip):
    try:
        # returns a single value
        response = requests.get("http://{ip}/api/system", timeout=5)
        return response.json
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


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
        fullpath = "/home/pi/solar-protocol/frontend/images/servers/" + filename
        filepath = "images/servers/" + filename
        # print("server:", server)
        myIP = requests.get("https://server.solarpowerforartists.com/?myip").text
        print("myIP", myIP)

        if "ip" in server:
            print("Server IP:", server["ip"])
            if server["ip"] == "localhost":  # if it is itself
                print("*** LOCAL HOST ***")
                # TODO: make this work with irregular ports
                image_path = imgDst
                filepath = image_path
            elif os.path.exists(fullpath):  # else if the image is in the folder
                print("Got image for " + server["name"])
            else:
                # else download image using api and save it to the folder: "../../frontend/images/servers/"
                image_path = "http://" + server["ip"] + "/local/serverprofile.gif"
                try:
                    download_file(image_path, fullpath)
                    print("image_path", image_path)
                    print("local_path", fullpath)
                except Exception as e:
                    print(server["name"], ": Offline. Can't get image")
            server["image_path"] = filepath


def main():

    print()
    print("***** Running create_html *****")
    print()

    energy_data = read_csv()  # get pv data from local csv
    local = get_local()  # get local steward data for front end
    api_key = "24df3e6ca023273cd426f67e7ac06ac9"
    try:
        local_weather = get_weather(lon=local.lon, lat=local.lat, api_key=api_key)
    except Exception as e:
        print(e)
        local_weather = {
            "description": "n/a",
            "temp": "n/a",
            "feels_like": "n/a",
            "sunrise": "n/a",
            "sunset": "n/a",
        }

    # 1. get IP list of addresses
    deviceList_data = get_ips()
    # creates deviceList_data
    print("#1")
    print(deviceList_data)
    print(deviceList_data.items())

    # 2 Collect data from all the difference servers on the network
    server_data = []

    for key, ip in deviceList_data.items():
        try:
            # item["ip"] = value #add IPs to server data
            [system] = getSystem(ip)
            # the above returns a dictionary containing all of the above system info
            # as documented here: http://solarprotocol.net/api/v1/
            # pvVoltage is a constant that is rated for the module.
            system["ip"] = ip
            # print("#2")
            # print(sInfo)
            # print(type(sInfo))
            server_data.append(system)

        except Exception as e:
            print(e)
            # reformat page so offline servers dont actually need this blank data?
            server_data.append(
                {
                    "ip": ip,
                    "name": key,
                    "description": "",
                    "city": "",
                    "location": "",
                    "country": "",
                }
            )

    # 3. get solar data and add it to server_data
    item_count = 0
    for item in server_data:
        try:
            solar_data = get_pv_value(item["ip"])
            # the above calls the api again. This returns the live PV voltage.
            status = "online"
        except Exception as e:
            solar_data = None
            status = "offline"
        item["solar_voltage"] = solar_data
        item["status"] = status
        try:
            time_stamp = getDeviceInfo("time stamp")
            if DEV:
                print("time_stamp!!!!!", time_stamp[item_count])

            ftime_stamp = datetime.datetime.fromtimestamp(
                float(time_stamp[item_count])
            ).strftime("%m/%d/%Y %H:%M:%S")
            if DEV:
                print(ftime_stamp)

            # time_stamp = ":".join(time_stamp.split(":")[0:-1])
        except Exception as e:
            ftime_stamp = "N/A"
        item["time_stamp"] = ftime_stamp

        # make lower case, remove spaces, remove nonstandard characters
        serverURL = "http://solarprotocol.net/network/" + re.sub(
            "[^A-Za-z0-9-_]+", "", item["name"].lower().replace(" ", "")
        )
        if status == "online":
            item["link"] = "<a href='" + serverURL + "'>" + serverURL + "</a>"
        else:
            item["link"] = serverURL
        item_count += 1

    # 4. get images and
    print("SERVER DATA!")
    print(server_data)
    local_data = get_local()
    check_images(server_data)
    render_pages(local_data, energy_data, local_weather, server_data)


if __name__ == "__main__":
    main()
