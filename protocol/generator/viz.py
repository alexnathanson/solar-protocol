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

w = 1500
h = 1500

Pi = 3.14159
hours = 72
ah = (2 * Pi) / hours  # angle of an hour
ring_rad = 61
radius = 61 * 10
start_ring = 0
DEBUG = "DEBUG" in os.environ

os.chdir(sys.path[0])  # if this script is called from a different directory

devices = "/data/devices.json"
imgDST = "/frontend/images"

energyParam = "PV-current"
ccDicts = []
days = 4  # get 4 days of csv files so we know we definitely get 72 hours of data

surface = gizeh.Surface(width=w, height=h)

# Get list of IP addresses that the pi can see
dfPOE = pd.DataFrame(columns=["device", "datetime"])

# -------------- FUNCTIONS --------------------------------------------------------------------------------

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []

    with open(devices) as f:
        data = json.load(f)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList


# Call API for every IP address and get charge controller data
def getCC(server, ccValue):
    print(f"GET {server} {ccValue}")
    url = f"http://{server}/api/v1/chargecontroller.php?value={ccValue}&duration={str(days)}"
    try:
        cc = requests.get(url, timeout=5)
        cc.json()
        return json.loads(cc.text)
    except JSONDecodeError as errj:
        print("A JSON decode error:" + repr(errj))
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError:
        print(f"Timed out connecting to {server}")
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# Call API for every IP address and get charge controller data
def getSysInfo(ip, key):
    url = f"http://{ip}/api/v1/chargecontroller.php?systemInfo={key}"
    try:
        sysinfo = requests.get(url, timeout=5)
        if DEBUG:
            print(f"{ip} {key}: {sysinfo.text}")
        return sysinfo.text
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError:
        print(f"Timed out connecting to {server}")
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))


# drawing the sunshine data (yellow)
def draw_ring(ccDict, ring_number, energy_parameter, timeZ, myTimeZone):
    if DEBUG:
        print(f"drawing text curve for {server_no} {message}")
    if type(ccDict) == type(None):
        return

    ccData = {}
    ccData["datetime"] = [
        datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f") for dt in ccDict.keys()
    ]
    ccData[energy_parameter] = [float(energy) for energy in ccDict.values()]

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
        if DEBUG:
            print("Current: ", current)
        draw_sun(ring_number, i, current)

    return df_hours


# draw_sun(ring number, x loc, y loc, stroke weight, _hour, _alpha)
def draw_sun(server_no, hour, alpha):
    a = -Pi / 2 + (hour * ah)
    sw = ring_rad
    arc = gizeh.arc(
        r=server_no * ring_rad - (ring_rad / 2) + (ring_rad * start_ring),
        xy=[w / 2, h / 2],
        a1=a,
        a2=a + ah,
        stroke=(1, 0.84, 0, alpha),
        stroke_width=sw,
    )
    arc.draw(surface)
    # DEBUGGING TEXT ON GRAPH
    # text = gizeh.text(str(alpha), fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy = [w/2+200, h/2])
    # text = text.rotate(a, center=[w/2, h/2]) # rotation around a center
    # text.draw(surface)


# def draw_server_arc(server_no, startAngle, stopAngle, color):
def draw_server_arc(server_no, start, stop, c):
    # Start in the center and draw the circle
    # print("server_no", server_no)
    # print("ring_rad", ring_rad)
    # print("stop", stop)
    # print("start", start)
    # print("c", c)
    if c == "Pink":
        return False

    if type(c) == type(" "):
        # print("Name!!", c)

        red, green, blue = webcolors.name_to_rgb(c)
        red = red / 255.0
        green = green / 255.0
        blue = blue / 255.0
        c = (red, green, blue)
        # print(c)

    circle = gizeh.arc(
        r=server_no * ring_rad + (0.5 + start_ring) * ring_rad,
        xy=[w / 2, h / 2],
        a1=stop - Pi / 2,
        a2=start - Pi / 2,
        stroke=c,
        stroke_width=15,
    )
    circle.draw(surface)


def sortPOE(logs, timeZones, myTimeZone):
    global dfPOE
    print("dfPOE.head()", dfPOE.head())
    for i, log in enumerate(logs):
        tempDF = pd.DataFrame(log)  # convert individual POE lists to dataframe
        tempDF["datetime"] = tempDF[0]
        # print("tempDF['datetime']")
        # print(tempDF['datetime'])
        tempDF["datetime"] = tempDF["datetime"].astype(
            str
        )  # convert entire "Dates" Column to string

        tempDF["datetime"] = pd.to_datetime(
            tempDF["datetime"], errors="coerce"
        )  # convert entire "Dates" Column to datetime format this time

        # shift by TZ
        tempDF["timedelta"] = pd.to_timedelta(tzOffset(timeZones[i], myTimeZone), "h")
        tempDF["datetime"] = tempDF["datetime"] + tempDF["timedelta"]
        tempDF = tempDF.drop(columns=["timedelta"])

        # tempDF['datetime'] = tempDF['datetime'] + relativedelta(hours=tzOffset(timeZones[l])) #shift by TZ
        tempDF = tempDF.drop(columns=[0])
        tempDF["device"] = i
        dfPOE = pd.concat([dfPOE, tempDF], ignore_index=True)
        dfPOE.shape

    # print(dfPOE.head())
    dfPOE = dfPOE.sort_values(by="datetime", ascending=False)
    # print(dfPOE.head())

    # get time now and filter by this time - 72 hours
    startTime = datetime.now()
    endTime = datetime.now() + relativedelta(days=-3)  # 3 days ago
    # print(dfPOE.shape)
    pastSeventyTwoHours = dfPOE["datetime"] > endTime
    dfPOE = dfPOE.loc[
        pastSeventyTwoHours
    ]  # filter out everything older than 3 days ago
    dfPOE = dfPOE.reset_index()
    # dfPOE = dfPOE.drop(columns=[0])

    # print(dfPOE.shape)

    dfPOE["percent"] = 0.0
    dfPOE["angle"] = 0

    if dfPOE.shape[0] > 0:
        for t in range(dfPOE.shape[0]):
            # print("start time:", startTime)
            # print("next time:", dfPOE['datetime'].iloc[t])
            minPast = ((startTime - dfPOE["datetime"].iloc[t]).total_seconds()) / 60
            # print("minutes since start:", minPast)
            # print("percent of the time:", minPast/(hours*60))
            dfPOE.at[t, "percent"] = minPast / (hours * 60)
            # print("percent again:", dfPOE['percent'].iloc[t])
            dfPOE.at[t, "angle"] = 360 - ((dfPOE["percent"].iloc[t]) * 360)
            # print("Angle:", dfPOE.at[t,'angle'])
    
    if DEBUG:
        print("head", dfPOE.head())
        print("tail", dfPOE.tail())

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
    offsetDir = 0
    if myOffset > theirOffset:
        offsetDir = 1
    else:
        offsetDir = -1
    return offsetDir * (
        abs((int(myOffset) / 100) - (int(theirOffset) / 100))
    )  # this only offsets to the hours... there are a few timezones in India and Nepal that are at 30 and 45 minutes


def text_curve(server_no, message, angle, spacing, ts):
    if DEBUG:
        print(f"drawing text curve for {server_no} {message}")
    cr = server_no * ring_rad + (ring_rad / 5) + (ring_rad * start_ring)
    # Start in the center and draw the circle
    # circle = gizeh.circle(r=cr-(ring_rad/2), xy = [w/2, h/2], stroke=(1,0,0), stroke_width= 1.5)
    # circle.draw(surface)
    # We must keep track of our position along the curve
    arclength = -10
    # For every letter
    for i in reversed(range(len(message))):
        currentChar = message[i]

        # print(message[i])
        # guessing the width of each char

        # Each box is centered so we move half the width
        arclength = arclength - spacing / 2
        # print("arclength")
        # print(arclength)
        # Angle in radians is the arclength divided by the radius
        # Starting on the left side of the circle by adding PI
        theta = (-1 / 2 * Pi) + arclength / cr + angle
        # print("theta")
        # print(theta)
        # Polar to cartesian coordinate conversion
        # add 250 so that the origin translates to center of screen, then add coords
        x = w / 2 + cr * math.cos(theta)
        y = h / 2 + cr * math.sin(theta)
        # Display the character

        text = gizeh.text(
            message[i].capitalize(),
            fontfamily="Georgia",
            fontsize=ts,
            fill=(1, 1, 1),
            xy=[x, y],
        )
        text = text.rotate(theta + (Pi / 2), center=[x, y])  # rotation around a center
        text.draw(surface)
        # popMatrix()
        # Move halfway again
        arclength -= spacing / 2


def lines(interval, sw, opacity):
    # for loop for lines
    a = -(Pi / 2)
    interval = (interval / 72) * 2 * Pi
    while a < (Pi * 2 - (Pi / 2)):
        xc = w / 2 + ring_rad * 2 * math.cos(a)
        yc = h / 2 + ring_rad * 2 * math.sin(a)
        x1 = w / 2 + (radius - 10) * math.cos(a)
        y1 = h / 2 + (radius - 10) * math.sin(a)
        line = gizeh.polyline(
            points=[(x1, y1), (xc, yc)], stroke_width=sw, stroke=(1, 1, 1, opacity)
        )
        line.draw(surface)
        a = a + interval
    # print("finished drawing lines")


def circles(sw, opacity):
    b = ring_rad * 2
    while b < (radius):
        circ = gizeh.circle(r=b, xy=[w / 2, h / 2], stroke=(1, 1, 1), stroke_width=1.5)
        circ.draw(surface)
        b = b + ring_rad

def getColor(ip):
    DEFAULT_COLOR = (1, 1, 1)
    try:
        color = getSysInfo(ip, "color")
    except:
        return DEFAULT_COLOR

    if type(color) == type(None) or color == "":
        return DEFAULT_COLOR
    
    return color

def getTimezone(ip):
    # defaults to NYC time - default to UTC in the future
    DEFAULT_TIMEZONE = "America/New_York"
    try:
        timezone = getSysInfo(ip, "tz")
    except:
        return DEFAULT_TIMEZONE

    if type(timezone) == type(None):
        return DEFAULT_TIMEZONE

    return timezone

def getCCDict(ip):
    DEFAULT_CCDICT = { "datetime": energyParam }
    ccDict = getCC(ip, energyParam)
    if type(ccDict) != type(None):
        # remove the header
        header = ccDict.pop("datetime", None)
        expected_header = energyParam.replace("-", " ")
        if header == expected_header:
            return ccDict
        
        return DEFAULT_CCDICT

# -------------- PROGRAM --------------------------------------------------------------------------------
def main():
    print()
    print("***** Running viz.py ******")
    print()

    ips = getDeviceInfo("ip")
    logs = getDeviceInfo("log")

    # in the future - convert everything from charge controller and poe log to UTC and then convert based on local time...
    timeZones = []
    myTimeZone = getSysInfo("localhost", "tz")

    colors = []

    # iterate through each device
    for ip in ips:
        if DEBUG:
            print(f"getting data for {ip}")

        ccDicts.append(getCCDict(ip))

        timeZones.append(getTimezone(ip))

        colors.append(getColor(ip))

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # customize inside labels
    server_names = getDeviceInfo("name")

    # go over ccDicts for each server
    for i, ccDict in enumerate(ccDicts):
        name = server_names[i]
        timezone = timeZones[i]
        if name not in ["pi-a", "pi-b", "pi-c"]:
            print(f"drawing {name} ({timezone})")
            # print name of each server
            text_curve(i + 2, name, 0, 18, 18)
            # draw sun data for each server
            draw_ring(ccDict, i + 3, energyParam, timezone, myTimeZone)

    # Draw Active Server Rings
    sortPOE(logs, timeZones, myTimeZone)
    # print("dfPOE.shape", dfPOE.shape)
    # print(dfPOE)
    # lines(interval in house, stroke weight, opacity)
    lines(2, 1, 0.2)
    lines(12, 1.5, 1)
    circles(1.5, 1)
    # draw_server_arc(0, 0, Pi, (1,0,0))

    if dfPOE.shape[1] > 0:
        # for l, item in enumerate(dfPOE.shape[0]):
        for l in range(dfPOE.shape[0]):
            device = dfPOE["device"].iloc[l]
            ring = device + 2
            server = colors[device]
            start_angle = dfPOE["angle"].iloc[l] * Pi / 180

            if l == 0:
                stop_angle = 2 * Pi
            else:
                stop_angle = dfPOE["angle"].iloc[l - 1] * Pi / 180

            draw_server_arc(ring, stop_angle, start_angle, server)

    # # initialize surface
    # surface = gizeh.Surface(width=w, height=h) # in pixels

    # text = gizeh.text("Hello World", fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy=(100,100), angle=Pi/12)
    # text.draw(surface)

    # draw_sun(4, w/2, h/2, 20, 0, 0.1)
    # draw_sun(4, w/2, h/2, 20, 1, 0.5)
    # draw_sun(4, w/2, h/2, 20, 2, 1)

    # #def text_curve(cr, message, angle, spacing, ts):
    # text_curve(100, "Server 1", 0, 0, 40)

    # draw_server_arc(2, 0, 3*Pi/2, (1,0,0))

    # Now export the surface
    surface.get_npimage()  # returns a (width x height x 3) numpy array
    surface.write_to_png("assets/clock.png")

    background = Image.open("assets/3day-diagram-with-key.png")
    exhibitionbackground = Image.open("assets/3day-diagram.png")
    foreground = Image.open("assets/clock.png")

    mask = Image.open("assets/mask.png").resize(background.size).convert("L")
    background.paste(foreground, (0, 0), mask)
    # this image goes to the frontend/images directory
    background.save(imgDST + "/clock.png")

    exhibitionbackground.paste(foreground, (0, 0), mask)
    # this image goes to the frontend/images directory
    exhibitionbackground.save(imgDST + "/clock-exhibit.png")

    # alphaBlended2 = Image.blend(foreground, background, alpha=.5)
    # alphaBlended2.save("clock1.png")
    # archive images
    now = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    archiveImage = Image.open(imgDST + "/clock.png")
    archiveImage.save(f"archive/clock-{now}.png")


if __name__ == "__main__":
    main()
