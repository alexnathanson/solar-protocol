from jinja2 import Template
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
            "batteryPercentage":  random.randint(0, 100),
        }
        print(data)
        return data


def read_csv():
    #filename = "../../charge-controller/data/tracerData2020-09-13.csv"
    filename = "../../charge-controller/data/tracerData"+str(datetime.date.today())+".csv"
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

def make_index(_local_data, _data, _hosting_data):
    if (_data["battery percentage"]) < 0.65:
        template_file = open("templates/index-small.html").read()
    else:
        template_file = open("templates/index-large.html").read()
    
    template = Template(template_file)
    rendered_html = template.render(
        date = _data["datetime"],
        solarVoltage=_data["PV voltage"], 
        batteryPercentage=_data["battery percentage"],
        loadVoltage=_data["load voltage"],
        loadCurrent= _data["load current"],
        hostingLog=_hosting_data,
        serverName=_local_data["name"]
    )
    # print(rendered_html)
    open("../../frontend/index.html", "w").write(rendered_html)


def get_hosting_log():
    filename = "../../backend/api/v1/hostList.json"
    with open(filename) as infile:
        data = json.load(infile)
    return data #array of dictionaries

def round_seconds(dts):
    result = []
    for item in dts:
        date = item.split()[0]
        h, m, s = [item.split()[1].split(':')[0],
                   item.split()[1].split(':')[1],
                   str(round(float(item.split()[1].split(':')[-1])))]
        result.append(date + ' ' + h + ':' + m + ':' + s)

    return result
    
def get_local():
    filename = "local.json"
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data #dictionary
 
    

def main():
    energy_data = read_csv()
    hosting_data = get_hosting_log()
    local_data = get_local()
    # print(hosting_data) 
    #print("Battery: {}".format(data("batteryPercentage"))
    #print("PV: {}".format(SolarVoltage))
    make_index(local_data, energy_data, hosting_data)
    
    #print(data)


if __name__ == "__main__":
    main()
