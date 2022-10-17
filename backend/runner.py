"""
This script controls when the other scripts run based on battery status and solar power
> 90% every 10 minutes
> 70% & <= 90% every 15 minutes
> 50% & <= 70% every 20 minutes
> 30% every 30 minutes
<= 30% every 60 minutes

pass the argument "now" to run everything immediately - otherwise sleep for 60 seconds before starting

If solar power production is 0 times are doubled.
If battery percentage is below 30, viz script doesn't run
"""
from core import clientPostIP
from core import solarProtocol
from core import getRemoteData
from core.SolarProtocolClass import SolarProtocol as SolarProtocolClass
from createHTML import create_html
from createHTML import viz
import datetime
import time
import sys
import logging
from math import trunc

SolarProtocol = SolarProtocolClass()

def run():
    print("***** Solar Protocol Runner Started ******")

    loopFrequency = getFrequency()
    print(f"Loop frequency: {str(loopFrequency)} minutes")
    scaler = solarScaler()
    timeOfRun = datetime.datetime.now()
    runNow = len(sys.argv) > 1 and sys.argv[1] == "now"

    if runNow:
        print("Running now")
    else:
        time.sleep(60)

    runScripts(False, 1)

    while True:
        if getElapsedTime(timeOfRun) % (loopFrequency * scaler) == 0:
            timeOfRun = datetime.datetime.now()
            runCount = runCount + 1

            # if we are on low power
            skipViz = loopFrequency == 60

            runScripts(skipViz, runCount)

            loopFrequency = getFrequency()
            print(f"Loop frequency: {str(loopFrequency)} minutes")

            scaler = solarScaler()

        time.sleep(60)

def runScripts(skipViz=False, runCount):
    time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    print(f"Run number {runCount} at {time}")

    exceptions = []

    try:
        clientPostIP.run()
    except Exception as err:
        printLoud("clientPostIP.py Exception", err)
        exceptions.append("clientPostIP")

    try:
        solarProtocol.run()
    except Exception as err:
        printLoud("solarProtocol.py Exception", err)
        exceptions.append("solarProtocol")

    try:
        getRemoteData.run()
    except Exception as err:
        printLoud("getRemoteData.py Exception", err)
        exceptions.append("getRemoteData")

    if not skipViz:
        try:
            viz.main()
        except Exception as err:
            printLoud("viz Exception", err)
            exceptions.append("viz")

    try:
        create_html.main()
    except Exception as err:
        printLoud("create_html Exception", err)
        exceptions.append("create_html")

    print()
    time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    print(f"Completed run {str(runCount)} at {time}")

    if len(exceptions) > 0:
        print("Exceptions:", " ".join(exceptions)
    else:
        print("Exceptions: 0, all good")

    print()

def printLoud(mess, e):
    print()
    print(f"!!!!! {mess} !!!!!")
    print(e)
    print()

def getElapsedTime(oldTime):
    """
    returns elapsed time since oldTime was set
    """
    elapsed = datetime.datetime.now() - oldTime
    elapsedMin = trunc(elapsed.seconds / 60)
    return elapsedMin

def getFrequency():
    """
    Set how frequent the script should run various functions
    """

    url = "http://localhost/api/v2/opendata.php?value=battery-percentage"

    try:
        battery_percentage = float(SP.getRequest(url))
        return 10 if battery_percentage > 0.9
        return 15 if battery_percentage > 0.7
        return 20 if battery_percentage > 0.5
        return 30 if battery_percentage > 0.3
        return 60
    except:
        return 20

def solarScaler():
    """
    solar power multiplier
    above 6 w it runs at the normal pace (the max power draw is about 5w)
    between 0 and 6 w it scales between the normal pace and 2x slower
    if 0w (i.e. no sun) the frequency slows down by 2
    """

    url = "http://localhost/api/v2/opendata.php?value=scaled-wattage"

    try:
        scaled_wattage = float(SolarProtocol.getRequest(url))
        return 1 if scaled_wattage >= 6.0
        return 1 + (1 - (scaled_wattage / 5.0)) if scaled_wattage >= 0.0
        return 2 if scaled_wattage == 0.0
    except:
        return 1

if __name__ == "__main__":
    run()
