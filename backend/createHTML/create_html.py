from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import datetime
import requests, json 
import json
import random
import csv


def get_data():
    client = ModbusClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
    client.connect()
    result = client.read_input_registers(0x3100, 16, unit=1)
    if not result.isError():
        solarVoltage = float(result.registers[0] / 100.0)
        solarCurrent = float(result.registers[1] / 100.0)
        solarPowerL = float(result.registers[2] / 100.0)
        solarPowerH = float(result.registers[3] / 100.0)
        batteryVoltage = float(result.registers[4] / 100.0)
        batteryCurrent = float(result.registers[5] / 100.0)
        batteryPowerL = float(result.registers[6] / 100.0)
        batteryPowerH = float(result.registers[7] / 100.0)
        loadVoltage = float(result.registers[8] / 100.0)
        loadCurrent = float(result.registers[9] / 100.0)
        loadPower = float(result.registers[10] / 100.0)

        result = client.read_input_registers(0x311A, 2, unit=1)
        batteryPercentage = float(result.registers[0] / 100.0)

        data = {
            "datetime": datetime.datetime.now(),
            "solarVoltage": solarVoltage,
            "solarCurrent": solarCurrent,
            "solarPowerL": solarPowerL,
            "solarPowerH": solarPowerH,
            "batteryVoltage": batteryVoltage,
            "batteryCurrent": batteryCurrent,
            "batteryPowerL": batteryPowerL,
            "batteryPowerH": batteryPowerH,
            "loadVoltage": loadVoltage,
            "loadCurrent": loadCurrent,
            "loadPower": loadPower,
            "batteryPercentage": batteryPercentage,
        }
        print(data)
        return data


def read_csv():
    # filename = "../../charge-controller/data/tracerData2020-09-13.csv"
    filename = (
        "../../charge-controller/data/tracerData" + str(datetime.date.today()) + ".csv"
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



def render_pages(_local_data, _data, _weather):
    print("Battery Percentage:" + str(_data["battery percentage"]))
    pages = [
        ("index_template.html", "index.html"),
        ("network_template.html", "network.html"),
        ("call_template.html", "call.html"),
        ("documentation_template.html", "documentation.html"),
        ("solar-web_template.html", "solar-web.html"),
        ("manifesto_template.html", "manifesto.html"),
    ]

    for template_filename, output_filename in pages:
        template_filename = "templates/" + template_filename
        output_filename = "../../frontend/" + output_filename
        template_file = open(template_filename).read()
        print("rendering", template_filename)
        print("battery", _data["battery percentage"]*100)
        template = Environment(loader=FileSystemLoader("templates/")).from_string(
            template_file
        )

        
        time = datetime.datetime.now()
        time = time.strftime("%I:%M %p")
        try:
            tz_url = "/api/v1/chargecontroller.php?systemInfo=tz"
            z = requests.get(tz_url) 
            zone = z.text
            zone = zone.replace('/', ' ')
            print("ZONE", zone)

        except Exception as e:
            zone = "TZ n/a"
        # print("ZONE", zone)

        # print("UTC TIME", datetime.datetime.utcnow())
        #would be nice to swap this out if the via script fails
        leadImage="images/clock.png"
        if((_data["battery percentage"]*100)>50):
            mode="High res mode"
        else:
            mode="Low res mode"
        

        # template = Template(template_file)
        rendered_html = template.render(
            time=time,
            solarVoltage=_data["PV voltage"],
            solarCurrent=_data["PV current"],
            solarPowerL=_data["PV power L"],
            solarPowerH=_data["PV power H"],
            batteryVoltage=_data["battery voltage"],
            batteryPercentage=_data["battery percentage"]*100,
            batterCurrent=_data["battery current"],
            loadVoltage=_data["load voltage"],
            loadCurrent=_data["load current"],
            loadPower=_data["load power"],
            name=_local_data["name"],
            description=_local_data["description"],
            location=_local_data["location"],
            city=_local_data["city"],
            country=_local_data["country"],
            lat=_local_data["lat"],
            long=_local_data["long"],
            bgColor=_local_data["bgColor"],
            serverColor=_local_data["serverColor"],
            font=_local_data["font"],
            borderStyle=_local_data["borderStyle"],
            weather=_weather["description"],
            temp=_weather["temp"],
            feelsLike=_weather["feels_like"],
            sunrise=_weather["sunrise"],
            sunset=_weather["sunset"],
            zone=zone,
            leadImage=leadImage,
            mode=mode
        )

        # print(rendered_html)
        open(output_filename, "w").write(rendered_html)

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


def get_local():
    filename = "../../../local/local.json"
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary


def main():
    energy_data = read_csv()
    local_data = get_local()
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
    # print(hosting_data)
    # print("Battery: {}".format(data("batteryPercentage"))
    # print("PV: {}".format(SolarVoltage))
    render_pages(local_data, energy_data, local_weather)

    # print(data)


if __name__ == "__main__":
    main()
