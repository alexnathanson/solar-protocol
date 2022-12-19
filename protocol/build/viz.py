import gizeh
import math
import os
import sys

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from PIL import Image
import webcolors

from pytz import timezone

import requests

import json
from json.decoder import JSONDecodeError

from logging import debug, exception, info

w = 1500
h = 1500

Pi = 3.14159
Tau = 2 * Pi
hours = 72
hour_angle = Tau / hours  # angle of an hour
ring_rad = 61
radius = 61 * 10
start_ring = 0

os.chdir(sys.path[0])  # if this script is called from a different directory

devices = "/data/devices.json"
imagePath = "/frontend/images"

energyParam = "PV current"
ccDicts = []
days = 4  # get 4 days of csv files so we know we definitely get 72 hours of data

surface = gizeh.Surface(width=w, height=h)

dfPOE = pd.DataFrame(columns=["device", "datetime"])

# -------------- FUNCTIONS --------------------------------------------------------------------------------

# Get device information
def getDeviceInfo(key):
    with open(devices) as file:
        data = json.load(file)

    deviceInfo = [device[key] for device in data]
    return deviceInfo


# Call API for every IP address and get charge controller data
def getChargeControllerValues(host: str):
    info(f"GET {host} charge-controller {energyParam} {days}")
    url = f"http://{host}/api/charge-controller"
    params = {"key": energyParam, "days": days}
    try:
        cc = requests.get(url, params, timeout=5)
        cc.json()
        return json.loads(cc.text)
    except JSONDecodeError:
        exception(f"JSON Decode Rrror")
    except requests.exceptions.HTTPError:
        exception(f"Http Error")
    except requests.exceptions.ConnectionError:
        exception(f"Connection Error to {host}")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


# Call API for every IP address and get charge controller data
def getSystem(server, key):
    url = f"http://{server}/api/system"
    params = {"key": key}
    try:
        systemInfo = requests.get(url=url, params=params, timeout=5)
        systemInfo = systemInfo.text

        info(f"{server} {key}: {systemInfo}")

        return systemInfo
    except requests.exceptions.HTTPError:
        exception(f"Http Error")
    except requests.exceptions.ConnectionError:
        exception(f"Connection Error to {server}")
    except requests.exceptions.Timeout:
        exception(f"Timeout")
    except requests.exceptions.RequestException:
        exception(f"Request Error")


# drawing the sunshine data (yellow)
def draw_ring(ccDict, ring_number, energy_parameter, timeZ, myTimeZone):
    info(f"drawing text curve for {ring_number}")
    if type(ccDict) == type(None):
        return

    ccData = {}
    ccData["datetime"] = [
        datetime.fromtimestamp(entry["timestamp"]) for entry in ccDict
    ]
    ccData[energy_parameter] = [entry[energy_parameter] for entry in ccDict]

    ccDataframe = pd.DataFrame.from_dict(ccData)

    # shift by TZ
    ccDataframe["timedelta"] = pd.to_timedelta(tzOffset(timeZ, myTimeZone), "h")
    ccDataframe = ccDataframe.drop(columns=["timedelta"])

    # replace index with entire "Dates" Column to work with groupby function
    ccDataframe.index = ccDataframe["datetime"]
    ccDataframe = ccDataframe.drop(columns=["datetime"])

    # take hourly average of multiple values
    df_hours = ccDataframe.groupby(pd.Grouper(freq="H")).mean()
    df_hours = df_hours.tail(72)  # last 72 hours

    df_hours[energy_parameter] = (
        df_hours[energy_parameter] / df_hours[energy_parameter].max()
    )

    # correlate sun data wtih colors
    for i, current in enumerate(df_hours[energy_parameter].tolist()):
        info(f"Current: {current}")
        draw_sun(ring_number, i, current)

    return df_hours


# draw_sun(ring number, x loc, y loc, stroke weight, _hour, _alpha)
def draw_sun(server_no, hour, alpha):
    a = -(Tau / 4) + (hour * hour_angle)
    sw = ring_rad
    arc = gizeh.arc(
        r=server_no * ring_rad - (ring_rad / 2) + (ring_rad * start_ring),
        xy=[w / 2, h / 2],
        a1=a,
        a2=a + hour_angle,
        stroke=(1, 0.84, 0, alpha),
        stroke_width=sw,
    )
    arc.draw(surface)
    # DEBUGGING TEXT ON GRAPH
    # text = gizeh.text(str(alpha), fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy = [w/2+200, h/2])
    # text = text.rotate(a, center=[w/2, h/2]) # rotation around a center
    # text.draw(surface)


def draw_server_arc(serverNumber, startAngle, stopAngle, color):
    if color == "Pink":
        return False

    # if color is a string, convert it
    if type(color) == type(" "):
        red, green, blue = webcolors.name_to_rgb(color)
        red = red / 255.0
        green = green / 255.0
        blue = blue / 255.0
        color = (red, green, blue)

    # Start in the center and draw the circle
    circle = gizeh.arc(
        r=serverNumber * ring_rad + (0.5 + start_ring) * ring_rad,
        xy=[w / 2, h / 2],
        a1=stopAngle - Tau / 4,
        a2=startAngle - Tau / 4,
        stroke=color,
        stroke_width=15,
    )
    circle.draw(surface)


def sortPOE(logs, timeZones, myTimeZone):
    global dfPOE

    for i, log in enumerate(logs):
        tempDF = pd.DataFrame(log)  # convert individual POE lists to dataframe
        tempDF["datetime"] = tempDF[0]

        # convert "Dates" Column to string
        tempDF["datetime"] = tempDF["datetime"].astype(str)

        # convert "Dates" Column to datetime format
        tempDF["datetime"] = pd.to_datetime(tempDF["datetime"], errors="coerce")

        # shift by TZ
        tempDF["timedelta"] = pd.to_timedelta(tzOffset(timeZones[i], myTimeZone), "h")
        tempDF["datetime"] = tempDF["datetime"] + tempDF["timedelta"]
        tempDF = tempDF.drop(columns=["timedelta"])

        # tempDF['datetime'] = tempDF['datetime'] + relativedelta(hours=tzOffset(timeZones[l])) #shift by TZ
        tempDF = tempDF.drop(columns=[0])
        tempDF["device"] = i
        dfPOE = pd.concat([dfPOE, tempDF], ignore_index=True)
        dfPOE.shape

    dfPOE = dfPOE.sort_values(by="datetime", ascending=False)

    # get time now and filter by this time - 72 hours
    startTime = datetime.now()
    endTime = datetime.now() + relativedelta(days=-3)  # 3 days ago

    pastSeventyTwoHours = dfPOE["datetime"] > endTime
    # filter out everything older than 3 days ago
    dfPOE = dfPOE.loc[pastSeventyTwoHours]
    dfPOE = dfPOE.reset_index()

    dfPOE["percent"] = 0.0
    dfPOE["angle"] = 0

    if dfPOE.shape[0] > 0:
        for t in range(dfPOE.shape[0]):
            nextTime = dfPOE["datetime"].iloc[t]
            minPast = ((startTime - nextTime).total_seconds()) / 60

            percentTime = minPast / (hours * 60)
            dfPOE.at[t, "percent"] = percentTime

            percent = dfPOE["percent"].iloc[t]
            dfPOE.at[t, "angle"] = 360 - (percent * 360)

    debug(f"head {dfPOE.head()}")
    debug(f"tail {dfPOE.tail()}")


def tzOffset(checkTZ, myTimeZone):
    try:
        myOffset = datetime.now(timezone(myTimeZone)).strftime("%z")
        myOffset = int(myOffset)
    except:
        myOffset = 0

    try:
        theirOffset = datetime.now(timezone(checkTZ)).strftime("%z")
        theirOffset = int(theirOffset)
    except:
        theirOffset = 0

    # this only offsets to the hours... there are a few timezones in India and Nepal that are at 30 and 45 minutes
    offsetHours = abs((int(myOffset) / 100) - (int(theirOffset) / 100))
    offsetDirection = 1 if myOffset > theirOffset else -1
    return offsetDirection * offsetHours


def text_curve(serverNumber, message, angle, spacing, fontsize):
    info(f"drawing text curve for {serverNumber} {message}")
    cr = serverNumber * ring_rad + (ring_rad / 5) + (ring_rad * start_ring)

    # Start in the center and draw the circle
    # circle = gizeh.circle(r=cr-(ring_rad/2), xy = [w/2, h/2], stroke=(1,0,0), stroke_width= 1.5)
    # circle.draw(surface)
    # We must keep track of our position along the curve
    arclength = -10
    # For every letter
    for i in reversed(range(len(message))):
        currentChar = message[i]

        # guessing the width of each char
        # Each box is centered so we move half the width
        arclength = arclength - spacing / 2

        # Angle in radians is the arclength divided by the radius

        # Starting on the left side of the circle by adding one full turn
        theta = (-1 / Tau) + (arclength / cr) + angle

        # Polar to cartesian coordinate conversion
        # add 250 so that the origin translates to center of screen, then add coords
        x = w / 2 + cr * math.cos(theta)
        y = h / 2 + cr * math.sin(theta)

        # Display the character
        text = gizeh.text(
            message[i].capitalize(),
            fontfamily="Georgia",
            fontsize=fontsize,
            fill=(1, 1, 1),
            xy=[x, y],
        )
        text = text.rotate(theta + (Tau / 4), center=[x, y])  # rotation around a center
        text.draw(surface)
        # popMatrix()

        # Move halfway again
        arclength -= spacing / 2


def lines(interval, stroke_width, opacity):
    # for loop for lines
    angle = -(Tau / 4)
    interval = (interval / 72) * Tau
    while angle < (Tau - (Tau / 4)):
        xc = w / 2 + ring_rad * 2 * math.cos(angle)
        yc = h / 2 + ring_rad * 2 * math.sin(angle)
        x1 = w / 2 + (radius - 10) * math.cos(angle)
        y1 = h / 2 + (radius - 10) * math.sin(angle)
        line = gizeh.polyline(
            points=[(x1, y1), (xc, yc)],
            stroke_width=stroke_width,
            stroke=(1, 1, 1, opacity),
        )
        line.draw(surface)
        angle = angle + interval


def circles():
    r = ring_rad * 2
    while r < radius:
        circle = gizeh.circle(
            r=r, xy=[w / 2, h / 2], stroke=(1, 1, 1), stroke_width=1.5
        )
        circle.draw(surface)
        r = r + ring_rad


def getColor(ip):
    DEFAULT_COLOR = (1, 1, 1)
    try:
        color = getSystem(ip, "color")
    except:
        return DEFAULT_COLOR

    if type(color) == type(None) or color == "":
        return DEFAULT_COLOR

    return color


def getTimezone(ip):
    # defaults to NYC time - default to UTC in the future
    DEFAULT_TIMEZONE = "America/New_York"
    try:
        timezone = getSystem(ip, "tz")
    except:
        return DEFAULT_TIMEZONE

    if type(timezone) == type(None):
        return DEFAULT_TIMEZONE

    return timezone


def getEnergyFor(host: str):
    energyValues = getChargeControllerValues(host)

    if type(energyValues) == type(None):
        return []

    return energyValues


# -------------- PROGRAM --------------------------------------------------------------------------------
def main():
    info("***** Running viz.py ******")

    ips = getDeviceInfo("ip")
    logs = getDeviceInfo("log")

    # in the future - convert everything from charge controller and poe log to UTC and then convert based on local time...
    timeZones = []
    myTimeZone = os.environ.get("TZ", "America/New_York")
    energyValues = []

    colors = []

    debug("ips are:")
    debug(ips)

    # iterate through each device
    for ip in ips:
        info(f"getting data for {ip}")

        energyValues.append(getEnergyFor(ip))

        timeZones.append(getTimezone(ip))

        colors.append(getColor(ip))

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # customize inside labels
    server_names = getDeviceInfo("name")

    # go over ccDicts for each server
    for i, energyValue in enumerate(energyValues):
        name = server_names[i]
        timezone = timeZones[i]
        info(f"drawing {name} ({timezone})")
        # print name of each server
        text_curve(i + 2, name, 0, 18, 18)
        # draw sun data for each server
        draw_ring(energyValue, i + 3, energyParam, timezone, myTimeZone)

    # Draw Active Server Rings
    sortPOE(logs, timeZones, myTimeZone)

    lines(interval=2, stroke_width=1, opacity=0.2)
    lines(interval=12, stroke_width=1.5, opacity=1)
    circles()

    if dfPOE.shape[1] > 0:
        for i in range(dfPOE.shape[0]):
            device = dfPOE["device"].iloc[i]
            ring = device + 2
            color = colors[device]
            startDegrees = 360 if i == 0 else dfPOE["angle"].iloc[i - 1]
            startAngle = startDegrees * Tau / 360
            stopAngle = dfPOE["angle"].iloc[i] * Tau / 360

            draw_server_arc(
                serverNumber=ring,
                startAngle=startAngle,
                stopAngle=stopAngle,
                color=color,
            )

    # setup file paths
    clockPath = f"{imagePath}/clock.png"
    exhibitPath = f"{imagePath}/clock-exhibit.png"
    now = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    archivePath = f"{imagePath}/archive/clock-{now}.png"

    assetsPath = "/protocol/build/assets"
    # export the clock surface
    surface.get_npimage()  # returns a (width x height x 3) numpy array
    surface.write_to_png(f"{assetsPath}/clock.png")

    background = Image.open(f"{assetsPath}/3day-diagram-with-key.png")
    exhibitionbackground = Image.open(f"{assetsPath}/3day-diagram.png")
    foreground = Image.open(f"{assetsPath}/clock.png")
    mask = Image.open(f"{assetsPath}/mask.png").resize(background.size).convert("L")

    # create the website clock
    background.paste(foreground, (0, 0), mask)
    background.save(clockPath)

    # create the exhibition clock
    exhibitionbackground.paste(foreground, (0, 0), mask)
    exhibitionbackground.save(exhibitPath)

    # copy the current clock to the archive
    archiveImage = Image.open(clockPath)
    archiveImage.save(archivePath)


if __name__ == "__main__":
    main()
