# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
import time
import datetime
import random
import csv
import os
import signal
import sys
from logging import info
from solar_common import fieldnames

PLATFORM = os.environ.get("PLATFORM", "unknown")
RASPBERRY_PI = PLATFORM == "pi"

FAKE_DATA = os.environ.get("FAKE_DATA", "False") == "True"

CONNECT = RASPBERRY_PI and not FAKE_DATA

if CONNECT:
    from pymodbus.client import ModbusSerialClient

def handle_exit(sig, frame):
    if CONNECT:
        client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def writeOrAppend(row):
    """
    create a new file daily to save data or append if the file already exists
    """
    fileName = f"/data/charge-controller/{datetime.date.today()}.csv"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(row)

    info(f"csv writing: {datetime.datetime.now()}")


def randomReadable(start: int, end: int):
    return round(random.uniform(start, end))


def readFromRandom():
    return {
        "timestamp": time.time(),
        "PV voltage": randomReadable(9, 30),
        "PV current": randomReadable(0, 2),
        "PV power L": randomReadable(28, 34),
        "PV power H": randomReadable(0, 1),
        "battery voltage": randomReadable(11, 15),
        "battery current": randomReadable(2, 3),
        "battery power L": randomReadable(28, 32),
        "battery power H": randomReadable(0, 1),
        "load voltage": randomReadable(12, 16),
        "load current": randomReadable(0, 1),
        "load power": randomReadable(3, 5),
        "battery percentage": 0.42069,
    }


def readFromDevice():
    controller = client.read_input_registers(0x3100, 16, 1)
    battery = client.read_input_registers(0x311A, 2, 1)

    if controller.isError():
        error(controller)
    if battery.isError():
        error(battery)
    if battery.isError() or controller.isError():
        return

    def toPercent(number):
        return float(number / 100.0)

    registers = controller.registers

    data = dict(zip(fieldnames, registers[0:10]))
    data["timestamp"] = time.time()
    data["battery percentage"] = toPercent(battery.registers[0])
    return data


if CONNECT:
    client = ModbusSerialClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200)
    try:
        client.connect()
    except err:
        error(f"Could not connect to charge controller! Set FAKE_DATA=True to ignore this")
        error(err)
        sys.exit(1)



if __name__ == "__main__":
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")
    print(f"{PLATFORM=} {RASPBERRY_PI=} {FAKE_DATA=} {CONNECT=}")

    read = readFromDevice if CONNECT else readFromRandom

    while True:
        sample = read()
        writeOrAppend(row=sample)
        time.sleep(secs=60 * 2)
