# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
import time
import datetime
import random
import csv
import os
import signal
import sys
from logging import error, info

from pymodbus.client.serial import ModbusSerialClient
from ..common.sample import fieldnames, Sample

from pydantic import TypeAdapter, ValidationError

def writeOrAppend(sample: Sample):
    """
    create a new file daily to save data or append if the file already exists
    """
    fileName = f"data/charge-controller/{datetime.date.today()}.csv"
    with open(fileName, "a+", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow(sample)

    info(f"csv writing: {datetime.datetime.now()}")

def randomBetween(start: int, end: int) -> int:
    return round(random.uniform(start, end))

def readFromRandom() -> Sample:
    return {
        "timestamp": time.time(),
        "PV voltage": randomBetween(9, 30),
        "PV current": randomBetween(0, 2),
        "PV power L": randomBetween(28, 34),
        "PV power H": randomBetween(0, 1),
        "battery voltage": randomBetween(11, 15),
        "battery current": randomBetween(2, 3),
        "battery power L": randomBetween(28, 32),
        "battery power H": randomBetween(0, 1),
        "load voltage": randomBetween(12, 16),
        "load current": randomBetween(0, 1),
        "load power": randomBetween(3, 5),
        "battery percentage": 0.42069,
    }

def readFromDevice(client: ModbusSerialClient) -> Sample | None:
    controller = client.read_input_registers(0x3100, 16, 1)
    battery = client.read_input_registers(0x311A, 2, 1)

    if controller.isError():
        error(controller)
    if battery.isError():
        error(battery)
    if battery.isError() or controller.isError():
        return None

    def toPercent(number):
        return float(number / 100.0)

    registers: list[float] = controller.registers

    data = dict(zip(fieldnames, registers[0:10]))
    data["timestamp"] = time.time()
    data["battery percentage"] = toPercent(battery.registers[0])

    sample_adapter = TypeAdapter(Sample)

    try:
        sample = sample_adapter.validate_python(data)
        return sample
    except ValidationError as err:
        error(err)

PLATFORM = os.environ.get("PLATFORM", "unknown")
RASPBERRY_PI = PLATFORM == "pi"
FAKE_DATA = os.environ.get("FAKE_DATA", "False") == "True"
CONNECT = RASPBERRY_PI and not FAKE_DATA

if __name__ == "__main__":
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
    print(f"{LOGLEVEL=}")
    logging.basicConfig(level=LOGLEVEL)
    print(f"{PLATFORM=} {RASPBERRY_PI=} {FAKE_DATA=} {CONNECT=}")

def run():
    client = ModbusSerialClient(method="rtu", port="/dev/ttyUSB0", baudrate=115200) if CONNECT else None
    if client:
        try:
            client.connect()
        except Exception as err:
            error("Error connecting to charge controller. Set FAKE_DATA=True to ignore")
            error(err)
            sys.exit(1)

    def handle_exit(sig, frame):
        if client: client.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    while True:
        sample = readFromDevice(client) if client else readFromRandom()
        if sample:
            writeOrAppend(sample)
        time.sleep(60 * 2)
