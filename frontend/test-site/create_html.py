from jinja2 import Template
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import datetime
import json 
import random

def get_data():
    client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 115200)
    client.connect()
    result = client.read_input_registers(0x3100,16,unit=1)
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

        result = client.read_input_registers(0x311A,2,unit=1)
        batteryPercentage = float(result.registers[0] / 100.0)

        
        data = {
            "datetime" : datetime.datetime.now(),
            "solarVoltage" : solarVoltage,
            "solarCurrent" : solarCurrent,
            "solarPowerL" : solarPowerL,
            "solarPowerH" : solarPowerH,
            "batteryVoltage" : batteryVoltage,
            "batteryCurrent" : batteryCurrent,
            "batteryPowerL" : batteryPowerL,
            "batteryPowerH" : batteryPowerH,
            "loadVoltage" : loadVoltage,
            "loadCurrent" : loadCurrent,
            "loadPower" : loadPower,
            "batteryPercentage" :  random.randint(0,100),
        }
        return data

def get_dummy_data():
    with open('../../charger-controller/data/tracerData2020-05-17.json') as d:
        result = json.load(d)
        n=0
        if d:
            #print("No data")
            solarVoltage = result[n]["solarVoltage"]
            solarCurrent = result[n]["solarCurrent"]
            solarPowerL = result[n]["solarPowerL"]
            solarPowerH = result[n]["solarPowerH"]
            batteryVoltage = result[n]["batteryVoltage"]
            batteryCurrent = result[n]["batteryCurrent"]
            batteryPowerL = result[n]["batteryPowerL"]
            batteryPowerH = result[n]["batteryPowerH"]
            loadVoltage = result[n]["loadVoltage"]
            loadCurrent = result[n]["loadCurrent"]
            loadPower = result[n]["loadPower"]
            batteryPercentage = result[n]["batteryPercentage"]

        # result = client.read_input_registers(0x311A,2,unit=1)
        # batteryPercentage = float(result["registers"][0] / 100.0)

        
        data = {
            "datetime" : datetime.datetime.now(),
            "solarVoltage" : solarVoltage,
            "solarCurrent" : solarCurrent,
            "solarPowerL" : solarPowerL,
            "solarPowerH" : solarPowerH,
            "batteryVoltage" : batteryVoltage,
            "batteryCurrent" : batteryCurrent,
            "batteryPowerL" : batteryPowerL,
            "batteryPowerH" : batteryPowerH,
            "loadVoltage" : loadVoltage,
            "loadCurrent" : loadCurrent,
            "loadPower" : loadPower,
            "batteryPercentage" :  random.randint(0, 100),
        }
        return data


def check_energy(_data):
    if _data["batteryPercentage"] < 50:
        print("Generating small page")
        template_file = open("templates/index-small.html").read()
        template = Template(template_file)
        rendered_html = template.render(solarVoltage=_data["solarVoltage"], batteryCurrent=_data["batteryCurrent"])
        print(rendered_html)
        open("output/index.html", "w").write(rendered_html)
    else: 
        print("Generating large page")
        template_file = open("templates/index-large.html").read()
        template = Template(template_file)
        rendered_html = template.render(solarVoltage=_data["solarVoltage"], batteryCurrent=_data["batteryCurrent"])
        print(rendered_html)
        open("output/index.html", "w").write(rendered_html)
    

def main():
    data = get_dummy_data()
    print(data["batteryPercentage"])
    check_energy(data)
    #print(data)


    


if __name__ == "__main__":
    main()