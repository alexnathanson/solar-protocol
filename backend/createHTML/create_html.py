# To run in dev mode from from virtual env:
#
#     source venv/bin/activate
#     python3 create_html.py DEV

# jinja reference: https://jinja.palletsprojects.com/en/3.0.x/templates/

from collections import UserList
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from glob import glob
import datetime
import requests, json 
import json
import csv
import os
import re
import sys

os.chdir(sys.path[0]) # if this script is called from a different directory
DEV = os.environ.get("ENV") == "DEV" or 'DEV' in sys.argv

root = f'/home/pi/solar-protocol/'
now = str(datetime.date.today())

dstIP = []
serverNames = []
myIP = " "
days = 3

#Call API for every IP address and get charge controller data 
def getCC(dst,ccValue):
    print("GET from " + dst)
    try:
        x = requests.get('http://' + dst + "/api/v1/chargecontroller.php?value=" + ccValue + "&duration=" + str(days), timeout=5)
        return json.loads(x.text)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

#gets power data from charge controller
def read_csv(): 
    chargeControllerData = f'{root}/charge-controller/data/tracerData{now}.csv'
    filename = (chargeControllerData)

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
    print("Battery Percentage:" + str(_data["battery percentage"]))

    templatePath = f'{root}/backend/createHTML/templates/'
    outputPath = f'{root}/frontend'

    pages = [
        ("index_template.html", "index.html"),
        ("network_template.html", "network.html"),
        ("call_template.html", "call.html"),
        ("documentation_template.html", "documentation.html"),
        ("solar-web_template.html", "solar-web.html"),
        ("manifesto_template.html", "manifesto.html"),
        ("library_template.html", "library.html"),
    ]

    #get the current time
    time = datetime.datetime.now()
    time = time.strftime("%I:%M %p")

    #get the timezone
    try:
        tz_url = "http://localhost/api/v1/chargecontroller.php?systemInfo=tz"
        z = requests.get(tz_url) 
        #for whatever reason, 404 errors weren't causing exceptions on Windows devices so this was added
        if z.status == 404:
            print("TZ 404 error")
            zone = "TZ n/a"
        else:
            zone = z.text
        #print("ZONE", z.text)
        zone = zone.replace('/', ' ')
        print("ZONE", zone)
    except Exception as e:
        print("Timezone Exception - TZ n/a")
        zone = "TZ n/a"
        #print("TZ na")

    # print("UTC TIME", datetime.datetime.utcnow())
    #would be nice to swap this out if the via script fails
    leadImage="images/clock.png"

    #determine mode
    if((_data["battery percentage"]*100)>30):
        mode="High res mode"
    else:
        mode="Low res mode"

    #loop through all page templates and render them with new data
    for template_filename, output_filename in pages:
        template_filename = templatePath + template_filename
        output_filename = outputPath + output_filename
        template_file = open(template_filename).read()
        print("rendering", template_filename)
        #print("battery", _data["battery percentage"]*100)
        #this line was changed last, it was: "/templates/"
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
            batteryPercentage=round(_data["battery percentage"]*100, 1),
            batterCurrent=_data["battery current"],
            loadVoltage=_data["load voltage"],
            loadCurrent=_data["load current"],
            loadPower=_data["load power"],
            name=_local_data["name"],
            #url=_local_data["url"],
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
            dev=' DEV' if DEV else '',
        )

        # print(rendered_html)
        open(output_filename, "w").write(rendered_html)

#get weather data
def get_weather(_local_data):
    api_key = "24df3e6ca023273cd426f67e7ac06ac9"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    lat = _local_data["lat"]
    lon = _local_data["long"]
    complete_url = base_url + "lon=" + lon+  "&lat=" +lat + "&appid=" + api_key 
    print(complete_url)

    response = requests.get(complete_url)
    x = response.json()  
    y = x["main"] 
    current_temperature = y["temp"] 
    current_humidiy = y["humidity"] 
    z = x["weather"] 
    weather_description = z[0]["description"] 

    sunrise=datetime.datetime.fromtimestamp(x["sys"]["sunrise"])
    sunset=datetime.datetime.fromtimestamp(x["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")


    print(" Temperature (in kelvin unit) = " +
                str(current_temperature) +
        "\n humidity (in percentage) = " +
                str(current_humidiy) +
        "\n description = " +
                str(weather_description)) 
   
    output = {
        "description": x["weather"][0]["description"],
        "temp": round(x["main"]["temp"]-273.15, 1),
        "feels_like": round(x["main"]["feels_like"]-273.15, 1),
        "sunrise": sunrise,
        "sunset": sunset,
    }

    return output

#get local front end data
def get_local():
    filename = f'{root}/local/local.json'
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []
    deviceList = f'{root}/backend/data/deviceList.json'

    with open(deviceList) as f:
      data = json.load(f)
      #print("Device list data:")
      #print(data)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList


def get_ips():
    # deviceInfoFile = "/home/pi/solar-protocol/backend/data/deviceList.json"
    # deviceInfo = json.dumps(deviceInfoFile)
    #Get my ip
    myIP = 	requests.get('https://server.solarpowerforartists.com/?myip').text
    #print("MY IP: ", type(myIP))

    #Get IPs, using keyword ip
    dstIP = getDeviceInfo('ip')
    for index, item in enumerate(dstIP):
        print(item)
        if(item == myIP):
            print("Replacing ip of self")
            dstIP[index]="localhost"

    log = getDeviceInfo('log')
    serverNames = getDeviceInfo('name')
    print (dstIP)
    print (serverNames)
    deviceList_data = dict(zip(serverNames, dstIP))
    print (deviceList_data)
    return deviceList_data


def active_servers(dst):
    try:
        x = requests.get("http://" + dst + "/local",timeout=5)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


#Call API for every IP address and get charge controller data 
def get_pv_value(dst):
    try:
        x = requests.get('http://' + dst + "/api/v1/api.php?value=PV-voltage",timeout=5)
        return x.text
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

#return data from a particular server
def getAPIData(apiEndPoint, dst):
    try:
        #returns a single value
        response = requests.get('http://' + dst + '/api/v1/'+apiEndPoint, timeout = 5)
        return response.text
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

def download_file(url, local_filename=None):
    #Downloads a file from a remote URL
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
        filename = server["name"]+".gif"
        filename = filename.replace(" ", "-")
        fullpath = "/home/pi/solar-protocol/frontend/images/servers/" + filename
        filepath = "images/servers/" + filename
        #print("server:", server)
        if "ip" in server:
            myIP = 	requests.get('https://server.solarpowerforartists.com/?myip').text
            print("Server IP:", server["ip"])
            print("myIP", myIP)
            if server["ip"] == "localhost": #if it is itself
                print("*** LOCAL HOST ***")
                #image_path = "home/pi/local/www/serverprofile.gif"
                image_path = imgDst
                #this wont work with irregular ports
                #image_path = "http://localhost/local/serverprofile.gif"
                filepath = image_path
            elif os.path.exists(fullpath): #else if the image is in the folder
                print("Got image for", server["name"])
            else: #else download image using api and save it to the folder: "../../frontend/images/servers/"
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
    
    energy_data = read_csv() #get pv data from local csv 
    local_data = get_local() #get local steward data for front end
    try:
        local_weather = get_weather(local_data) 
    except Exception as e:
        print(e)
        local_weather = {
            "description": "n/a",
            "temp": "n/a",
            "feels_like": "n/a",
            "sunrise": "n/a",
            "sunset": "n/a"
        }

    #1. get IP list of addresses
    deviceList_data = get_ips()
    #creates deviceList_data
    print("#1")
    print(deviceList_data)
    print(deviceList_data.items())
  
    #2 Collect data from all the difference servers on the network
    server_data = []

    for key, value in deviceList_data.items():
        try:
            # item["ip"] = value #add IPs to server data
            sInfo = json.loads(getAPIData('chargecontroller.php?systemInfo=dump',value))
            # the above returns a dictionary containing all of the above system info
            # as documented here: http://solarprotocol.net/api/v1/
            # pvVoltage is a constant that is rated for the module.
            sInfo['ip'] = value
            # print("#2")
            # print(sInfo)
            # print(type(sInfo))
            server_data.append(sInfo)

        except Exception as e:
            print(e)
            #reformat page so offline servers dont actually need this blank data?
            server_data.append({'ip':value,'name':key, 'description':'', 'city':'', 'location':'','country':''})

    #3. get solar data and add it to server_data
    item_count = 0
    for item in server_data:
        try:
            solar_data = get_pv_value(item["ip"]) 
            #the above calls the api again. This returns the live PV voltage.
            status = "online"
        except Exception as e:
            solar_data = None
            status = "offline"
        item["solar_voltage"] = solar_data
        item["status"] = status
        try: 
            time_stamp = getDeviceInfo('time stamp')
            print("time_stamp!!!!!!!!!!!!!!!!!!!!", time_stamp[item_count])
         
            ftime_stamp = datetime.datetime.fromtimestamp(float(time_stamp[item_count])).strftime("%m/%d/%Y %H:%M:%S")
            print(ftime_stamp)

            #time_stamp = ":".join(time_stamp.split(":")[0:-1])
        except Exception as e:
            ftime_stamp = "N/A"
        item["time_stamp"] = ftime_stamp

        #make lower case, remove spaces, remove nonstandard characters 
        serverURL = 'http://solarprotocol.net/network/' + re.sub('[^A-Za-z0-9-_]+', '', item["name"].lower().replace(" ",""))
        if status == "online":
            item["link"] =  "<a href='" + serverURL + "'>" + serverURL +"</a>"
        else:
            item["link"] = serverURL
        item_count += 1

    #4. get images and 
    print("SERVER DATA!")
    print(server_data)
    check_images(server_data)
    render_pages(local_data, energy_data, local_weather, server_data)


if __name__ == "__main__":
    main()
