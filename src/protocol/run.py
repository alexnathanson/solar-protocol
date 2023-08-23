"""
This script controls when the other scripts run based on battery status and solar power
> 90% every 10 minutes
> 70% & <= 90% every 15 minutes
> 50% & <= 70% every 20 minutes
> 30% every 30 minutes
<= 30% every 60 minutes

If the photovoltaic wattage is below 6W, run half as often
If battery percentage is below 30%, viz script doesn't run
"""

from .build import html, viz
from .core import publishDevice, solarProtocol, getRemoteData

import datetime
import requests
import logging
import os

from time import sleep
from math import trunc
from logging import info, debug, error, exception
from typing import Union

one_minute = 60
MAX_FREQUENCY = one_minute

LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
logging.basicConfig(level=LOGLEVEL)
print(f"{LOGLEVEL=}")


def run():
    info("***** Solar Protocol Runner Started ******")

    # Wait for the api to be ready
    while True:
        try:
            requests.get("http://127.0.0.1:11215/api/devices", timeout=None)
            break
        except requests.ConnectionError:
            sleep(5)

    info("api ready")

    runCount = 0
    scaler = None
    timeOfRun = None
    loopFrequency = None
    while True:
        if runCount == 0 or getElapsedTime(timeOfRun) % (loopFrequency * scaler) == 0:
            timeOfRun = datetime.datetime.now()
            runCount = runCount + 1

            runScripts(runCount)

            loopFrequency = getFrequency()
            info(f"{loopFrequency=} minutes")
            scaler = solarScaler()
        sleep(one_minute)


def runScripts(runCount):
    time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    debug(f"Run number {runCount} at {time}")

    # if we are on low power
    skipViz = getFrequency == MAX_FREQUENCY

    exceptions = []

    try:
        publishDevice.run()
    except Exception:
        exception("publishDevice exception")
        exceptions.append("publishDevice")

    # FIXME: Explain why do we run solarProtocol before getRemoteData?
    try:
        solarProtocol.run()
    except Exception:
        exception("solarProtocol exception")
        exceptions.append("solarProtocol")

    try:
        getRemoteData.run()
    except Exception:
        exception("getRemoteData exception")
        exceptions.append("getRemoteData")

    if not skipViz:
        try:
            viz.main()
        except Exception:
            exception("viz exception")
            exceptions.append("viz")

    try:
        html.main()
    except Exception:
        exception("html exception")
        exceptions.append("html")

    time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    info(f"Completed run {str(runCount)} at {time}")

    if len(exceptions) > 0:
        exceptionString = " ".join(exceptions)
        error(f"Exceptions: {exceptionString}")
    else:
        info("Exceptions: 0, all good")


def getElapsedTime(oldTime):
    """
    returns elapsed time since oldTime was set
    """
    elapsed = datetime.datetime.now() - oldTime
    elapsedMin = trunc(elapsed.seconds / one_minute)
    return elapsedMin


def getFrequency() -> Union[10, 15, 20, 30, MAX_FREQUENCY]:
    """
    Set how frequent the script should run various functions
    """

    url = "http://localhost:11215/api/charge-controller"
    params = {"key": "battery percentage"}

    try:
        response = requests.get(url=url, params=params)
        [latest] = response.json()
        battery_percentage = latest.battery_percentage
        return 10 if battery_percentage > 0.9 else None
        return 15 if battery_percentage > 0.7 else None
        return 20 if battery_percentage > 0.5 else None
        return 30 if battery_percentage > 0.3 else None
        return MAX_FREQUENCY
    except Exception:
        return 20


def solarScaler() -> Union[1, 2, None]:
    """
    solar power multiplier
    above 6 w it runs at the normal pace (the max power draw is about 5w)
    between 0 and 6 w it scales between the normal pace and 2x slower
    if 0w (i.e. no sun) the frequency slows down by 2
    """

    url = "http://localhost/api/charge-controller"
    params = {"key": "scaled wattage"}

    try:
        response = requests.get(url=url, params=params)
        [latest] = response.json()
        scaled_wattage = latest.scaled_wattage
        return 1 if scaled_wattage >= 6.0 else None
        return 1 + (1 - (scaled_wattage / 5.0)) if scaled_wattage >= 0.0 else None
        return 2 if scaled_wattage == 0.0 else None
    except Exception:
        return 1


if __name__ == "__main__":
    run()
