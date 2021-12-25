
import gizeh as g
import math

import pandas as pd
import json
import datetime
from dateutil.relativedelta import relativedelta
from PIL import Image
import webcolors

from pytz import timezone
import pytz

import requests
from json.decoder import JSONDecodeError

import sys

w = 1500
h = 1500

Pi = 3.14159
hours = 72
ah = (2*Pi)/hours #angle of an hour
ring_rad = 61 
radius = 61*10
start_ring = 1

#Run settings
local = 1
debug_mode = 0

# path = "/home/pi/solar-protocol/backend"
# if local == 1:
#     path = "../"   

path = "/home/pi/solar-protocol/backend"
if local == 0:
    path = ".."   

#Global variables
deviceList = path + "/data/deviceList.json"


energyParam = "PV-current"
ccData = []
days = 4 # get 4 days of csv files so we know we definitely get 72 hours of data

surface = g.Surface(width=w, height=h)

# Get list of IP addresses that the pi can see
dfPOE = pd.DataFrame(columns = ['device', 'datetime']) 

#Array for server names
serverNames = ["Server 1", "Server 2"]

# -------------- FUNCTIONS --------------------------------------------------------------------------------

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []

    with open(deviceList) as f:
      data = json.load(f)
      print("Device List data:")
    #   print(data)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList

#Call API for every IP address and get charge controller data 
def getCC(dst,ccValue):
    print("GET from " + dst)
    try:
        x = requests.get('http://' + dst + "/api/v1/chargecontroller.php?value="+ccValue + "&duration="+str(days),timeout=5)
        #print("API charge controller data:")
        #print(x.text)
        x.json()
        return json.loads(x.text)
    except JSONDecodeError as errj:
        print("A JSON decode error:" + repr(errj))
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

#Call API for every IP address and get charge controller data 
def getSysInfo(dst,k):
    try:
        x = requests.get('http://' + dst + "/api/v1/chargecontroller.php?systemInfo="+k,timeout=5)
        if (debug_mode):
            print("API system data:")
            # print(json.loads(x.text))
        return x.text
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

#drawing the sunshine data (yellow)
def draw_ring(ccDict, ring_number, energy_parameter,timeZ, myTimeZone):

    ccDataframe = pd.DataFrame.from_dict(ccDict, orient="index")

    ccDataframe.columns = ccDataframe.iloc[0]
    ccDataframe = ccDataframe.drop(ccDataframe.index[0])
    ccDataframe = ccDataframe.reset_index()
    ccDataframe.columns = ['datetime',energy_parameter]
    if (debug_mode):
        print("ccDataframe.head()")
        print(ccDataframe.head())

    ccDataframe['datetime'] = ccDataframe['datetime'].astype(str) #convert entire "Dates" Column to string 
    ccDataframe['datetime']=pd.to_datetime(ccDataframe['datetime']) #convert entire "Dates" Column to datetime format this time 
    
    #shift by TZ
    ccDataframe['timedelta'] = pd.to_timedelta(tzOffset(timeZ, myTimeZone),'h')
    ccDataframe['datetime'] = ccDataframe['datetime'] + ccDataframe['timedelta'] 
    ccDataframe = ccDataframe.drop(columns=['timedelta'])
    
    ccDataframe[energy_parameter] = ccDataframe[energy_parameter].astype(float) #convert entire column to float
    ccDataframe.index=ccDataframe['datetime'] #replace index with entire "Dates" Column to work with groupby function
    ccDataframe = ccDataframe.drop(columns=['datetime'])
    df_hours = ccDataframe.groupby(pd.Grouper(freq='H')).mean() #take hourly average of multiple values
    df_hours = df_hours.tail(72) # last 72 hours
    #print("DF Hours: ", df_hours)

    df_hours[energy_parameter] = df_hours[energy_parameter] / df_hours[energy_parameter].max()

    # #correlate sun data wtih colors 
    for i, current in enumerate(df_hours[energy_parameter].tolist()):
        if (debug_mode):
            print("Current: ", current)
        draw_sun(ring_number, i, current) 

    return df_hours

# draw_sun(ring number, x loc, y loc, stroke weight, _hour, _alpha)
def draw_sun(server_no, hour, alpha):
    a = -Pi/2 + (hour*ah)
    sw = ring_rad
    arc = g.arc(r = server_no*ring_rad-(ring_rad/2)+(ring_rad*start_ring), xy = [w/2, h/2], a1 = a, a2 = a+ah , stroke=(1, 0.84, 0, alpha), stroke_width= sw)
    arc.draw(surface)
    #DEBUGGING TEXT ON GRAPH
    # text = g.text(str(alpha), fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy = [w/2+200, h/2])
    # text = text.rotate(a, center=[w/2, h/2]) # rotation around a center
    # text.draw(surface)

#def draw_server_arc(server_no, startAngle, stopAngle, color):
def draw_server_arc(server_no, start, stop, c):
  # Start in the center and draw the circle
    # print("server_no", server_no)
    # print("ring_rad", ring_rad)
    # print("stop", stop)
    # print("start", start)
    # print("c", c)
    if c == "Pink":
        return False

    if type(c)==type(" "):
        #print("Name!!", c)
            
        red, green, blue = webcolors.name_to_rgb(c)
        red = red/255.0
        green = green/255.0
        blue = blue/255.0
        c=(red, green, blue)
        #print(c)



    circle = g.arc(r=server_no*ring_rad+(0.5+start_ring)*ring_rad, xy = [w/2, h/2], a1 = stop-Pi/2, a2 = start-Pi/2, stroke=c, stroke_width= 15)
    circle.draw(surface)  

def sortPOE(log, timeZones, myTimeZone):
    global dfPOE
    print(dfPOE.head())
    for l in range(len(log)):
        tempDF = pd.DataFrame(log[l]) #convert individual POE lists to dataframe
        tempDF['datetime'] = tempDF[0]
        # print("tempDF['datetime']")
        # print(tempDF['datetime'])
        tempDF['datetime'] = tempDF['datetime'].astype(str) #convert entire "Dates" Column to string 

        tempDF['datetime']=pd.to_datetime(tempDF['datetime'], errors="coerce") #convert entire "Dates" Column to datetime format this time 

         #shift by TZ
        tempDF['timedelta'] = pd.to_timedelta(tzOffset(timeZones[l], myTimeZone),'h')
        tempDF['datetime'] = tempDF['datetime'] + tempDF['timedelta'] 
        tempDF = tempDF.drop(columns=['timedelta'])

        #tempDF['datetime'] = tempDF['datetime'] + relativedelta(hours=tzOffset(timeZones[l])) #shift by TZ
        tempDF = tempDF.drop(columns=[0])
        tempDF['device'] = l
        dfPOE = dfPOE.append(tempDF, ignore_index=True)
        dfPOE.shape

    #print(dfPOE.head())
    dfPOE = dfPOE.sort_values(by='datetime',ascending=False)
    #print(dfPOE.head())

    #get time now and filter by this time - 72 hours
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now() + relativedelta(days=-3) #3 days ago
    #print(dfPOE.shape)
    pastSeventyTwoHours = (dfPOE['datetime'] > endTime)
    dfPOE = dfPOE.loc[pastSeventyTwoHours] #filter out everything older than 3 days ago
    dfPOE = dfPOE.reset_index()
    #dfPOE = dfPOE.drop(columns=[0])

    #print(dfPOE.shape)

    dfPOE['percent']=0.0
    dfPOE['angle']=0

    if dfPOE.shape[0] > 0:
        for t in range(dfPOE.shape[0]):
            #print("start time:", startTime)
            #print("next time:", dfPOE['datetime'].iloc[t])
            minPast = ((startTime - dfPOE['datetime'].iloc[t]).total_seconds())/60
            #print("minutes since start:", minPast)
            #print("percent of the time:", minPast/(hours*60))
            dfPOE.at[t,'percent']= minPast/ (hours*60)
            #print("percent again:", dfPOE['percent'].iloc[t])
            dfPOE.at[t,'angle'] = 360-((dfPOE['percent'].iloc[t])*360)
            #print("Angle:", dfPOE.at[t,'angle'])

    #print(dfPOE.head())
    #print(dfPOE.tail())

def tzOffset(checkTZ, myTimeZone):
    try:
        myOffset = datetime.datetime.now(pytz.timezone(myTimeZone)).strftime('%z')
        myOffset = int(myOffset)
    except: 
        myOffset = 0
    try:
        theirOffset = datetime.datetime.now(pytz.timezone(checkTZ)).strftime('%z')
        theirOffset = int(theirOffset)
    except: 
        theirOffset = 0
    offsetDir = 0
    if myOffset > theirOffset:
        offsetDir = 1
    else:
        offsetDir = -1 
    return offsetDir*(abs((int(myOffset)/100) - (int(theirOffset)/100)))#this only offsets to the hours... there are a few timezones in India and Nepal that are at 30 and 45 minutes


def text_curve(server_no, message, angle, spacing, ts):
    cr = server_no*ring_rad+(ring_rad/5)+(ring_rad*start_ring)
  # Start in the center and draw the circle
    # circle = g.circle(r=cr-(ring_rad/2), xy = [w/2, h/2], stroke=(1,0,0), stroke_width= 1.5)
    # circle.draw(surface)
    # We must keep track of our position along the curve
    arclength = - 10
    # For every letter
    for i in reversed(range(len(message))):
        currentChar = message[i]

        # print(message[i])
        # guessing the width of each char

        # Each box is centered so we move half the width
        arclength = arclength - spacing/2
        # print("arclength")
        # print(arclength)
        # Angle in radians is the arclength divided by the radius
        # Starting on the left side of the circle by adding PI
        theta = (-1/2*Pi) + arclength / cr + angle  
        # print("theta")
        # print(theta)
        # Polar to cartesian coordinate conversion
        # add 250 so that the origin translates to center of screen, then add coords
        x = w/2 + cr * math.cos(theta)
        y = h/2 + cr * math.sin(theta)
        # Display the character
        
        text = g.text(message[i].capitalize(), fontfamily="Georgia",  fontsize=ts, fill=(1,1,1), xy = [x, y])
        text = text.rotate(theta+(Pi/2), center=[x,y]) # rotation around a center
        text.draw(surface)
        # popMatrix()
        # Move halfway again
        arclength -= spacing/2

def lines(interval, sw, opacity):
        #for loop for lines 
    a = -(Pi/2)
    interval = (interval/72)*2*Pi
    while a < (Pi*2-(Pi/2)):
        xc = w/2 + ring_rad*2 * math.cos(a)
        yc = h/2 + ring_rad*2 * math.sin(a)
        x1 = w/2 + (radius-10) * math.cos(a)
        y1 = h/2 + (radius-10) * math.sin(a)
        line = g.polyline(points=[(x1,y1), (xc,yc)], stroke_width=sw, stroke=(1,1,1,opacity))
        line.draw(surface)
        a = a + interval
    # print("finished drawing lines")

def circles(sw, opacity):
    b = ring_rad*2
    while b < (radius):
        circ = g.circle(r=b, xy = [w/2, h/2], stroke=(1,1,1), stroke_width= 1.5)
        circ.draw(surface)
        b = b + ring_rad

 
    
# -------------- PROGRAM --------------------------------------------------------------------------------
# -------------- PROGRAM --------------------------------------------------------------------------------
def main():
    # print("current sys path (viz): " + sys.path)

    #Get my ip
    myIP = 	requests.get('http://whatismyip.akamai.com/').text
    # print("MY IP: ", type(myIP))

    #Get IPs, using keyword ip
    dstIP = getDeviceInfo('ip')
    for index, item in enumerate(dstIP):
        # print(item)
        if(item == myIP):
            # print("Replacing ip of self")
            dstIP[index]="localhost"

    log = getDeviceInfo('log')
    serverNames = getDeviceInfo('name')

    # print (dstIP)
    # print (serverNames)

    #in the future - convert everything from charge controller and poe log to UTC and then convert based on local time...
    timeZones = []
    myTimeZone = getSysInfo("localhost",'tz')
    # print("My TZ: ", myTimeZone)

    sysC = []

    # dstIP = dstIP[0:1]

    #iterate through each device
    for i in dstIP:
        #print(i)
        # if i not in activeIPs:
        #     activeIPs.append(i)
        getResult = getCC(i, energyParam)
        if type(getResult) != type(None):
            ccData.append(getResult)
        else:
            ccData.append({"datetime": energyParam})
        try:
            tempTZ = getSysInfo(i, 'tz')
        except: 
            tempTZ = 'America/New_York' 

        if type(tempTZ) != type(None):
            timeZones.append(tempTZ)
        else:
            timeZones.append('America/New_York')#defaults to NYC time - default to UTC in the future

        try:
            tempC = getSysInfo(i,'color')
        except:
            tempC = (1,1,1)
        
        if type(tempC) == type(None) or tempC == '':
            tempC = (1,1,1)
        sysC.append(tempC) 

    # print(timeZones)

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    #customize inside labels
    server_names = getDeviceInfo('name')
    # print("server names", len(server_names))

    # go over ccData for each server
    for i, item in enumerate(ccData):

        # print name of each server
        text_curve(i+2, server_names[i], 0, 18, 18)
        #draw sun data for each server
        draw_ring(item,i+3, energyParam,timeZones[i], myTimeZone)


    #Draw Active Server Rings
    sortPOE(log, timeZones, myTimeZone)
    # print("dfPOE.shape", dfPOE.shape)
    # print(dfPOE)
    #lines(interval in house, stroke weight, opacity)
    lines(2, 1, 0.2)
    lines(12, 1.5, 1)
    circles(1.5, 1)
    # draw_server_arc(0, 0, Pi, (1,0,0))

    if dfPOE.shape[1] > 0:
        #for l, item in enumerate(dfPOE.shape[0]):
        for l in range(dfPOE.shape[0]):
            if l == 0:
                # print("Server:" ,sysC[dfPOE['device'].iloc[l]])
                # print( sysC[dfPOE['device'].iloc[l]])
                # print("First Angle:", dfPOE['angle'].iloc[l])
                draw_server_arc(dfPOE['device'].iloc[l]+2, 2*Pi, dfPOE['angle'].iloc[l]*(Pi/180), sysC[dfPOE['device'].iloc[l]])
            else:
                # print( sysC[dfPOE['device'].iloc[l]])
                # print("Server:" ,sysC[dfPOE['device'].iloc[l]])
                # print("ring:", dfPOE['device'].iloc[l])
                # print("start arc:", dfPOE['angle'].iloc[l])
                # print("stop arc:", dfPOE['angle'].iloc[l-1])
                draw_server_arc(dfPOE['device'].iloc[l]+2, dfPOE['angle'].iloc[l-1]*Pi/180, dfPOE['angle'].iloc[l]*Pi/180, sysC[dfPOE['device'].iloc[l]])


    # # initialize surface
    # surface = g.Surface(width=w, height=h) # in pixels

    # text = g.text("Hello World", fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy=(100,100), angle=Pi/12)
    # text.draw(surface)




    # draw_sun(4, w/2, h/2, 20, 0, 0.1) 
    # draw_sun(4, w/2, h/2, 20, 1, 0.5) 
    # draw_sun(4, w/2, h/2, 20, 2, 1) 

    # #def text_curve(cr, message, angle, spacing, ts):
    # text_curve(100, "Server 1", 0, 0, 40)

    # draw_server_arc(2, 0, 3*Pi/2, (1,0,0))

    # Now export the surface
    surface.get_npimage() # returns a (width x height x 3) numpy array
    surface.write_to_png("clock.png")



    background = Image.open(path+"/visualization/3day-diagram-nolabels1.png")
    exhibitionbackground = Image.open(path+"/visualization/3day-diagram-nolabels1-nokey.png")
    foreground = Image.open("clock.png")


    mask = Image.open(path+'/visualization/mask5.png').resize(background.size).convert('L')
    background.paste(foreground, (0, 0), mask)
    background.save(path+"/../frontend/images/clock.png")

    exhibitionbackground.paste(foreground, (0, 0), mask)
    exhibitionbackground.save(path+"/../frontend/images/clock-exhibit.png")

    # alphaBlended2 = Image.blend(foreground, background, alpha=.5)
    # alphaBlended2.save("clock1.png")
    #archive images
    archiveImage = Image.open(path+"/../frontend/images/clock.png")
    archiveImage.save(path+'/visualization/archive/clock-' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +'.png') #archive plot


if __name__ == "__main__":
    #this enables the relative paths to work when running this directly from command line
    # sys.path.append('createHTML')

    main()
