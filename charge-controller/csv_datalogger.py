# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import datetime
import numpy as np
import pandas as pd
import csv
import os

client = ModbusClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
client.connect()

while True:
    result = client.read_input_registers(0x3100, 16, unit=1)
    result2 = client.read_input_registers(0x311A, 2, unit=1)

    if not result.isError() and not result2.isError():
        pvVoltage = float(result.registers[0] / 100.0)
        pvCurrent = float(result.registers[1] / 100.0)
        pvPowerL = float(result.registers[2] / 100.0)
        pvPowerH = float(result.registers[3] / 100.0)
        batteryVoltage = float(result.registers[4] / 100.0)
        batteryCurrent = float(result.registers[5] / 100.0)
        batteryPowerL = float(result.registers[6] / 100.0)
        batteryPowerH = float(result.registers[7] / 100.0)
        loadVoltage = float(result.registers[8] / 100.0)
        loadCurrent = float(result.registers[9] / 100.0)
        loadPower = float(result.registers[10] / 100.0)

        batteryPercentage = float(result2.registers[0] / 100.0)

        newDF = pd.DataFrame(
            data={
                "datetime": [datetime.datetime.now()],
                "PV voltage": [pvVoltage],
                "PV current": [pvCurrent],
                "PV power L": [pvPowerL],
                "PV power H": [pvPowerH],
                "battery voltage": [batteryVoltage],
                "battery current": [batteryCurrent],
                "battery power L": [batteryPowerL],
                "battery power H": [batteryPowerH],
                "load voltage": [loadVoltage],
                "load current": [loadCurrent],
                "load power": [loadPower],
                "battery percentage": [batteryPercentage],
            }
        )

        # create a new file daily to save data
        # or append if the file already exists
        fileName = f"/data/traces/{str(datetime.date.today())}.csv"
        try:
            with open(fileName) as csvfile:
                df = pd.read_csv(fileName)
                df = df.append(newDF, ignore_index=True)
                df.to_csv(fileName, sep=",", index=False)
        except:
            newDF.to_csv(fileName, sep=",", index=False)

        print(f"csv writing: {str(datetime.datetime.now())")

    else:
        print(f"error: {result}")

    # runs every 2 minutes
    sleep(60 * 2)

client.close()
