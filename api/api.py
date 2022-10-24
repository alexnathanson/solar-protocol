import csv
from datetime import date
from enum import Enum
from typing import Union
import sys

from fastapi import FastAPI

fieldnames = [
    "timestamp",
    "PV voltage",
    "PV current",
    "PV power L",
    "PV power H",
    "battery voltage",
    "battery current",
    "battery power L",
    "battery power H",
    "load voltage",
    "load current",
    "load power",
    "battery percentage",
]

class CCValue(str, Enum):
    PV_voltage = "PV voltage"
    PV_current = "PV current"
    PV_power_L = "PV power L"
    PV_power_H = "PV power H"
    battery_voltage = "battery voltage"
    battery_current = "battery current"
    battery_power_L = "battery power L"
    battery_power_H = "battery power H"
    load_voltage = "load voltage"
    load_current = "load current"
    load_power = "load power"
    battery_percentage = "battery percentage"


app = FastAPI(title="solar-protocol", docs_url="/api/docs")


@app.get("/api")
def root():
    return {"message": "Hello World 👋"}


@app.get("/api/charge-controller")
def read_value(value: Union[CCValue, None] = None):

    filename = f"/data/traces/{date.today()}.csv"

    rows = []

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
        for row in reader:
            rows.append(row)

    if value == None:
        return row

    return row[value]

    # return rows
    # print(csv, file=sys.stderr)
    # return ["assassin", "cleric", "druid", "fighter", "illusionist",
    #        "magic_user", "thief", "paladin", "ranger"]

    # line = read_csv()
    # print(line[-1])
