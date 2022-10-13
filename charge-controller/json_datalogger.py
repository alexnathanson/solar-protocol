# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import datetime
import os
import json
import collections as cl


# trick to write datetime to json
def json_serial(obj):
    if isinstance(obj, (datetime.datetime)):
        return obj.isoformat()


# create a new file daily to save data
# or append if the file already exists
def append_json_to_file(data: dict, path_file: str) -> bool:
    with open(path_file, "ab+") as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(json.dumps([data], default=json_serial).encode())
        else:
            f.seek(-1, 2)
            f.truncate()  # delete ']'
            f.write(" , ".encode())  # add ','
            f.write(json.dumps(data, default=json_serial).encode())
            f.write("]".encode())  # add ']'
    return f.close()


client = ModbusClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
client.connect()

while True:
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
        if not result.isError():
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

            # create a new file daily to save data
            # or append if the file already exists
            fileName = "data/tracerData" + str(datetime.date.today()) + ".json"
            append_json_to_file(data, fileName)

            # print(data)
            print("json writing: " + str(datetime.datetime.now()))

            # runs every x-seconds
            sleep(60 * 15)

    else:
        print("error: {}".format(result))


client.close()
