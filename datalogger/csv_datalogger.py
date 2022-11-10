# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
import time
import datetime
import random
import csv
import os
import sys
from solar_common import fieldnames

DEV = "DEV" in sys.argv

if not DEV:
    from pymodbus.client import ModbusSerialClient


def writeOrAppend(row):
    """
    create a new file daily to save data or append if the file already exists
    """
    fileName = f"/data/traces/{datetime.date.today()}.csv"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(row)

    print(f"csv writing: {datetime.datetime.now()}")


def readFromRandom():
    return {
        "timestamp": time.time(),
        "PV voltage": random.uniform(9, 30),
        "PV current": random.uniform(0, 2),
        "PV power L": random.uniform(28, 34),
        "PV power H": random.uniform(0, 1),
        "battery voltage": random.uniform(11, 15),
        "battery current": random.uniform(2, 3),
        "battery power L": random.uniform(28, 32),
        "battery power H": random.uniform(0, 1),
        "load voltage": random.uniform(12, 16),
        "load current": random.uniform(0, 1),
        "load power": random.uniform(3, 5),
        "battery percentage": random.uniform(0, 1),
    }


def readFromDevice():
    controller = client.read_input_registers(0x3100, 16, unit=1)
    battery = client.read_input_registers(0x311A, 2, unit=1)

    if controller.isError():
        print(f"error: {controller}")
    if battery.isError():
        print(f"error: {battery}")
    if battery.isError() or controller.isError():
        return

    def toPercent(number):
        return float(number / 100.0)

    registers = controller.registers.map(toPercent)

    data = dict(zip(fieldnames, registers[0:10]))
    data["timestamp"] = time.time()
    data["battery percentage"] = toPercent(battery)
    return data


if not DEV:
    client = ModbusSerialClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
    client.connect()

while True:
    read = readFromRandom if DEV else readFromDevice

    writeOrAppend(read())

    # runs every 2 minutes
    time.sleep(60 * 2)

client.close()
