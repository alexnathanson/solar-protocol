# To run in dev mode from from virtual env:
# source venv/bin/activate
# in unix/MacOS use this => ENV=DEV python3 create_html.py
# in windows use this => python3 create_html.py DEV

from collections import UserList
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client import ModbusSerialClient as ModbusClient
from glob import glob
import datetime
import requests, json 
import json
import csv
import os
import re
import sys

#jinja reference: https://jinja.palletsprojects.com/en/3.0.x/templates/

if os.environ.get("ENV") == "DEV" or 'DEV' in sys.argv:
    print('running in dev mode')
    path = ".." 
    rootPath = "../../"
    chargeControllerDataPath = rootPath + 'dev-data/'
    chargecontrollerdata = "testtracerdata"
    templatePath = "templates-sunthinking/"
    outputPath = rootPath + "frontend/sunthinking/"
    deviceList = rootPath + "/dev-data/deviceList.json"
    imgDst = rootPath + "frontend/images/servers/serverprofile.png"
    localDataSrc = chargeControllerDataPath
else:
    path = "/home/pi/solar-protocol/backend"
    rootPath = "/home/pi/"
    chargeControllerDataPath = rootPath + "solar-protocol/charge-controller/data/"
    chargecontrollerdata = "tracerData"+str(datetime.date.today()) 
    templatePath = path + "/createHTML/templates-sunthinking/"
    outputPath = rootPath + "solar-protocol/frontend/sunthinking/" 
    deviceList = path + "/data/deviceList.json"
    imgDst = "/home/pi/local/www/serverprofile.gif"
    localDataSrc = rootPath + "local/"

dstIP = []
serverNames = []
myIP = " "
days = 3



#gets power data from charge controller
def read_csv(): 
    try:
        # filename = "../../charge-controller/data/tracerData2020-09-13.csv"
        filename = (
            #rootPath + "solar-protocol/charge-controller/data/" + chargecontrollerdata + ".csv"
            chargeControllerDataPath + chargecontrollerdata + ".csv"
        )

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
    except:
        print("Error reading charge controller data from csv.") 


def render_pages(_local_data, _data, _weather,):
    try:
        print("Battery Percentage:" + str(_data["battery percentage"]))
    except:
        print("No energy data received.")

    pages = [
        ("index-template.html", "index.html"),
         ("networks-template.html", "networks.html"),
          ("interviews-template.html", "interviews.html"),
           ("projects-template.html", "projects.html"),
            ("essays-template.html", "essays.html"),
            ("materiality-template.html", "materiality.html"),
             ("limits-template.html", "limits.html"),
              ("intelligence-template.html", "intelligence.html"),
              ("solar-template.html", "solar.html"),
               ("situatedness-template.html", "situatedness.html"),

         ("pasek-template.html", "pasek.html"),
         ("parrish-template.html", "parrish.html"),
          ("adam-template.html", "adam.html"),
                      ("ash-template.html", "ash.html"),
             ("devalk-template.html", "devalk.html"),
              ("lenz-template.html", "lenz.html"),
              ("liu-template.html", "liu.html"),
               ("dick-template.html", "dick.html"),
                 ("zhang-template.html", "zhang.html"),
                           ("motaghy-fowler.html", "fowler.html"),
                           ("motaghy-kumar.html", "kumar.html"),
                           ("motaghy-dinesh.html", "dinesh.html"),
                           ("motaghy-smith.html", "smith.html"),
                           ("motaghy-zhang.html", "a-zhang.html"),
                            ("motaghy-template.html", "motaghy.html"),
           ("wamburu-template.html", "wamburu.html"),
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
    try:
        if((_data["battery percentage"]*100)>30):
            mode="High res mode"
        else:
            mode="Low res mode"
    except: 
        mode="High res mode"

    #loop through all page templates and render them with new data
    for template_filename, output_filename in pages:
        template_filename = templatePath + template_filename #path + "/createHTML/templates/" + template_filename
        output_filename = outputPath + output_filename #rootPath + "solar-protocol/frontend/" + output_filename
        template_file = open(template_filename).read()
        print("rendering", template_filename)
        #print("battery", _data["battery percentage"]*100)
        #this line was changed last, it was: "/templates/"
        template = Environment(loader=FileSystemLoader(path + "/createHTML/templates-sunthinking/")).from_string(
            template_file
        )
        
        try:
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

            )
        except:
            rendered_html = template.render(
                time=time,
                solarVoltage= "n/a",
                solarCurrent="n/a",
                solarPowerL="n/a",
                solarPowerH="n/a",
                batteryVoltage="n/a",
                batteryPercentage=50,
                batterCurrent="n/a",
                loadVoltage="n/a",
                loadCurrent="n/a",
                loadPower="n/a",
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

            )

        # print(rendered_html)
        open(output_filename, "w").write(rendered_html)

#get weather data
def get_weather(_local_data):
    api_key = _local_data["api_key"]
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    lat = _local_data["lat"]
    lon = _local_data["long"]
    complete_url = base_url + "lon=" + lon + "&lat=" + lat + "&appid=" + api_key
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
    filename = localDataSrc + "local.json"
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []

    with open(deviceList) as f:
      data = json.load(f)
      #print("Device list data:")
      #print(data)
    
    # Remove objects based on the key matching items in the deadIP Array
    data = [obj for obj in data if obj['ip'] not in deadIPs]

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
    # server_images_paths = glob("../../frontend/images/servers/*.jpg")
    # server_images_names = [os.path.basename(i) for i in server_images_paths]
    #server_images_names = server_images_paths.split("/")[-1]
    # ps.path.basename[image]
    for server in server_data:
        filename = server["name"]+".gif"
        filename = filename.replace(" ", "-")
        fullpath = rootPath + "solar-protocol/frontend/images/servers/" + filename
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
    print("***** Running create_sunthinking *****")
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


    render_pages(local_data, energy_data, local_weather)


if __name__ == "__main__":
    main()

