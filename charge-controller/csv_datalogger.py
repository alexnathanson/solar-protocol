# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import datetime
import numpy as np
import pandas as pd
import csv
import os
import sys

DEV = "DEV" in sys.argv or "DEV" in os.environ

def writeOrAppend(dataFrame):
    """
    create a new file daily to save data
    or append if the file already exists
    """
    fileName = f"/data/traces/{str(datetime.date.today())}.csv"
    try:
        with open(fileName) as csvfile:
            df = pd.read_csv(fileName)
            df = df.append(newDF, ignore_index=True)
            df.to_csv(fileName, sep=",", index=False)
    except:
        newDF.to_csv(fileName, sep=",", index=False)

    print(f"csv writing: {str(datetime.datetime.now())}")

def readFromRandom():
    return pd.DataFrame(
        data={
            "datetime": [datetime.datetime.now()],
            "PV voltage": [random.uniform(9,30)],
            "PV current": [random.uniform(0,2)],
            "PV power L": [random.uniform(28,34)],
            "PV power H": [random.uniform(0,1)],
            "battery voltage": [random.uniform(11,15)],
            "battery current": [random.uniform(2,3)],
            "battery power L": [random.uniform(28,32)],
            "battery power H": [random.uniform(0,1)],
            "load voltage": [random.uniform(12,16)],
            "load current": [random.uniform(0,1)],
            "load power": [random.uniform(3,5)],
            "battery percentage": [random.uniform(0,1)],
        }
    )

def readFromDevice():
    result = client.read_input_registers(0x3100, 16, unit=1)
    result2 = client.read_input_registers(0x311A, 2, unit=1)

    if result.isError() or result2.isError():
        print(f"error: {result}")
    else:
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

        return pd.DataFrame(
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

if not DEV:
  client = ModbusClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
  client.connect()

while True:
    read = readFromRandom if DEV else readFromDevice

    writeOrAppend(read())

    # runs every 2 minutes
    sleep(60 * 2)

client.close()
