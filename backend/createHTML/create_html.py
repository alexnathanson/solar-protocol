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


def make_index(_local_data, _data, _hosting_data):
    if (_data["battery percentage"]) < 0.65:
        template_file = open("templates/index-small.html").read()
    else:
        template_file = open("templates/index-large.html").read()

    template = Template(template_file)
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
        hostingLog=_hosting_data,
        serverName=_local_data["name"]
    )
    #print(rendered_html)
    open("../../frontend/index.html", "w").write(rendered_html)


def get_hosting_log():
    filename = "../../backend/api/v1/hostList.json"
    with open(filename) as infile:
        data = json.load(infile)
    return data  # array of dcitionaries


def update_hosting_log():
    #get device list data
    filename = "../../backend/api/v1/deviceList.json"
    with open(filename) as infile:
        data = json.load(infile)

    #get host list data (what is shown on the site)
    host_filename = "../../backend/api/v1/hostList.json"
    with open(host_filename) as infile:
        host_data = json.load(infile)
        last_change_timestamp=host_data[-1]

    #in device list, parse the time stamp data for each server into datetime objects
    date_time_str_1 = data[0]["log"][0]
    date_time_obj_1 = datetime.datetime.strptime(
        date_time_str_1, '%Y-%m-%d %H:%M:%S.%f')

    date_time_str_2 = data[1]["log"][1]
    date_time_obj_2 = datetime.datetime.strptime(
        date_time_str_2, '%Y-%m-%d %H:%M:%S.%f')

    date_time_str_3 = data[2]["log"][2]
    date_time_obj_3 = datetime.datetime.strptime(
        date_time_str_3, '%Y-%m-%d %H:%M:%S.%f')

    #compare each and get latest entry
    if(date_time_obj_1 > date_time_obj_2) and (date_time_obj_1 > date_time_obj_3):
        # print("1:"+date_time_str_1)
        latest_date = date_time_obj_1
        name = data[0]["ip"]
        host_data.append({
            "ip": name,
            "name": "TEST4",
            "time": date_time_str_1[0:-7]}
            )
    elif(date_time_obj_2 > date_time_obj_3):
        # print("2:"+date_time_str_2)
        latest_date = date_time_obj_2
        name = data[1]["ip"]
        host_data.append({
            "ip": name,
            "name": "TEST4",
            "time": date_time_str_2[0:-7]}
            )
    else:
        # print("3:"+date_time_str_3)
        latest_date = date_time_obj_3
        name = data[2]["ip"]
        host_data.append({
            "ip": name,
            "name": "TEST4",
            "time": date_time_str_3[0:-7]}
            )

#If the IP address for this entry is the same as the last in hostList, then no change in host.
    if(name==last_change_timestamp['ip']):
        print("No change in host.")

    else: #if they have changed, then host has been updated
        print("Change in host, updating host log")
        host_data=host_data[-12:]
        #print(type(date_time_str_1))
        #print(host_data)
        print("Started writing JSON data into a file")
        with open('../../backend/api/v1/hostList.json', 'w') as fp:
            json.dump(host_data, fp, indent=2)


def get_local():
    filename = "/home/pi/local/local.json"
    with open(filename) as infile:
        local_data = json.load(infile)
    return local_data  # dictionary


def main():
    energy_data = read_csv()
    update_hosting_log()
    hosting_data = get_hosting_log()
    local_data = get_local()
    # print(hosting_data)
    # print("Battery: {}".format(data("batteryPercentage"))
    #print("PV: {}".format(SolarVoltage))
    make_index(local_data, energy_data, hosting_data)

    # print(data)


if __name__ == "__main__":
    main()
