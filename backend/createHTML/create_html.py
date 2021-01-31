from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import datetime
import json
import random
import csv


def get_data():
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200)
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
            "batteryPercentage":  batteryPercentage,
        }
        print(data)
        return data


def read_csv():
    #filename = "../../charge-controller/data/tracerData2020-09-13.csv"
    filename = "../../charge-controller/data/tracerData" + \
        str(datetime.date.today())+".csv"
    with open(filename, 'r') as data:
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


def make_index(_local_data, _data):
    print("Battery Percentage:"+str(_data["battery percentage"]))
    if (_data["battery percentage"]) < 0.50:
        template_file = open("templates/index-small.html").read()
        print("Low res mode")
    else:
        template_file = open("templates/index-large.html").read()
        print("High res mode")

    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_file)

    #template = Template(template_file)
    rendered_html = template.render(
        date=_data["datetime"],
        solarVoltage=_data["PV voltage"],
        solarCurrent=_data["PV current"],
        solarpowerL=_data["PV power L"],
        solarpowerH=_data["PV power H"],
        batteryVoltage=_data["battery voltage"],
        batteryPercentage=_data["battery percentage"],
        batterCurrent= _data["battery current"],
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
        bgColor = _local_data["bgColor"],
        serverColor = _local_data["serverColor"],
        font = _local_data["font"],
        borderStyle = _local_data["borderStyle"]
    )
    #print(rendered_html)
    open("../../frontend/index.html", "w").write(rendered_html)


def get_local():
    filename = "../../../local/local.json"
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary


def main():
    energy_data = read_csv()
    local_data = get_local()
    # print(hosting_data)
    # print("Battery: {}".format(data("batteryPercentage"))
    #print("PV: {}".format(SolarVoltage))
    make_index(local_data, energy_data)

    # print(data)


if __name__ == "__main__":
    main()
