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
from typing import TypedDict

PLATFORM = os.environ.get("PLATFORM", "unknown")
RASPBERRY_PI = PLATFORM == "pi"

FAKE_DATA = os.environ.get("FAKE_DATA", "False") == "True"

CONNECT = RASPBERRY_PI and not FAKE_DATA

if CONNECT:
    from pymodbus.client import ModbusSerialClient


class Sample(
    TypedDict(
        "Sample",
        {
            timestamp: float,
            "PV voltage": float,
            "PV current": float,
            "PV power L": float,
            "PV power H": float,
            "battery voltage": float,
            "battery current": float,
            "battery power L": float,
            "battery power H": float,
            "load voltage": float,
            "load current": float,
            "load power": float,
            "battery percentage": float,
        },
    )
):
    pass


def writeOrAppend(sample: Sample):
    """
    create a new file daily to save data or append if the file already exists
    """
    fileName = f"/data/charge-controller/{datetime.date.today()}.csv"
    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(row)

    info(f"csv writing: {datetime.datetime.now()}")


def randomReadable(start: int, end: int) -> int:
    return round(random.uniform(start, end))


def readFromRandom() -> Sample:
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


def readFromDevice() -> Sample:
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
        error(
            f"Could not connect to charge controller! Set FAKE_DATA=True to ignore this"
        )
        error(err)
        sys.exit(1)


def handle_exit(sig, frame):
    if CONNECT:
        client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

read = readFromDevice if CONNECT else readFromRandom


def run():
    while True:
        writeOrAppend(read())
        time.sleep(60 * 2)


if __name__ == "__main__":
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    print(f"{LOGLEVEL=}")
    logging.basicConfig(level=LOGLEVEL)
    print(f"{PLATFORM=} {RASPBERRY_PI=} {FAKE_DATA=} {CONNECT=}")

run()
