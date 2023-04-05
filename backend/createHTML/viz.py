import gizeh as g
import math
import os
import sys

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


w = 1500
h = 1500

Pi = 3.14159
hours = 72
ah = (2*Pi)/hours #angle of an hour

ring_rad = 61
radius = ring_rad*10

key_ring_rad = 61  
key_radius = key_ring_rad*10
start_ring = 0
start_radius_data = 4
debug_mode =0

if os.environ.get("ENV") == "DEV" or 'DEV' in sys.argv:
    path = ".." 
    rootPath = "../.."
    deviceList = rootPath + "/dev-data/deviceList.json"
    imgDST = rootPath + "/dev-data/temp"
    print("Dev mode activated")
else:
    rootPath = "/home/pi/solar-protocol"
    path = "/home/pi/solar-protocol/backend"
    deviceList = path + "/data/deviceList.json"
    imgDST = rootPath + "/frontend/images"


energyParam = "PV-current"
ccData = []
days = 4 # get 4 days of csv files so we know we definitely get 72 hours of data

surface = g.Surface(width=w, height=h)

# Get list of IP addresses that the pi can see
dfPOE = pd.DataFrame(columns = ['device', 'datetime']) 

#Array for server names
serverNames = ["Server 1", "Server 2"]
server_cities = [" ", " "]

with open(path+'/createHTML/deadIPs.txt', 'r') as infile:
    deadIPs = infile.readlines()
    deadIPs = [d.strip() for d in deadIPs]


# -------------- FUNCTIONS --------------------------------------------------------------------------------

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []

    with open(deviceList) as f:
      data = json.load(f)
    #   print("Device List data:")
    #   print(data)

    # Remove objects based on the key matching items in the deadIP Array
    data = [obj for obj in data if obj['ip'] not in deadIPs]

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
    # df_hours = df_hours.tail(72) # last 72 hours
    df_hours = df_hours.tail(72)
    print("DF Hours: ", df_hours.shape)

    df_hours[energy_parameter] = df_hours[energy_parameter] / df_hours[energy_parameter].max()

    #correlate sun data with colors 
    for i, current in enumerate(df_hours[energy_parameter].tolist()):
        if (debug_mode):
            print("Current: ", current)
        draw_sun(ring_number, i, current, ring_rad) 

    return df_hours

# draw_sun(ring number, x loc, y loc, stroke weight, _hour, _alpha)
def draw_sun(server_no, hour, alpha, rad):
    a = -Pi/2 + (hour*ah)
    sw = rad
    arc = g.arc(r = server_no*rad-(rad/2)+(rad*start_ring), xy = [w/2, h/2], a1 = a, a2 = a+ah , stroke=(1, 0.84, 0, alpha), stroke_width= sw)
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


def text_curve(server_no, message, angle, spacing, ts, rad):
    print('running text_curve: ' + message)
    cr = server_no*rad+(rad/5)+(rad*start_ring)
  # Start in the center and draw the circle
    # circle = g.circle(r=cr-(ring_rad/2), xy = [w/2, h/2], stroke=(1,0,0), stroke_width= 1.5)
    # circle.draw(surface)
    # We must keep track of our position along the curve
    arclength = - 10
    # For every letter
    for i in reversed(range(len(message))):
        print(i)
        currentChar = message[i]
        print(currentChar)
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
    s = 7
    interval = (interval/72)*2*Pi
    while a < (Pi*2-(Pi/2)):
        if a>-(Pi/2):
            s=sw
        xc = w/2 + ring_rad*4 * math.cos(a)
        yc = h/2 + ring_rad*4 * math.sin(a)
        x1 = w/2 + (radius-10) * math.cos(a)
        y1 = h/2 + (radius-10) * math.sin(a)
        line = g.polyline(points=[(x1,y1), (xc,yc)], stroke_width=s, stroke=(1,1,1,opacity))
        line.draw(surface)
        a = a + interval
    # print("finished drawing lines")

def circles(sw, opacity):
    b = ring_rad*4
    while b < (radius):
        circ = g.circle(r=b, xy = [w/2, h/2], stroke=(1,1,1), stroke_width= 1.5)
        circ.draw(surface)
        b = b + ring_rad

def drawPOEKey(sysC):
    start_angle = Pi/3+Pi/16
        
    for col in sysC:

        draw_server_arc(1.5, start_angle, start_angle-Pi/8, col)
        start_angle = start_angle-Pi/8

    text_curve(1.8,"TIME AS ACTIVE SERVER:", start_angle, 13, 18, key_ring_rad)

    text_curve(1.3,"SUNLIGHT AT EACH SERVER:", 0, 13, 18, key_ring_rad)
    al = 0.1
    for i in range(14):
        draw_sun(1.7, i, al, key_ring_rad)
        al = al + 0.1

    text_curve(2.3,"------------------------------KEY-------------------------------KEY-------------------------------KEY", 0, 10, 18, ring_rad)


    
# -------------- PROGRAM --------------------------------------------------------------------------------
# -------------- PROGRAM --------------------------------------------------------------------------------
def main():
    print()
    print("***** Running viz.py ******")
    print()

    # print("current sys path (viz): " + sys.path)

    

    print("deadIPs:")
    print(deadIPs)
    #Get my ip
    myIP = 	requests.get('https://server.solarpowerforartists.com/?myip').text
    # print("MY IP: ", type(myIP))

    #Get IPs, logs and names from deviceList file, using keyword ip
    dstIP = getDeviceInfo('ip')
    log = getDeviceInfo('log')
    server_names = getDeviceInfo('name')
    print(dstIP)
    #replace own ip with local host
    for index, item in enumerate(dstIP):
        print(item)
        if(item == myIP):
            # print("Replacing ip of self")
            dstIP[index]="localhost"


    print("IP List:")
    print (dstIP)
    print (server_names)

    # ring_rad=95-(6*len(dstIP))

    print("ring radius:")
    print(ring_rad)

    #in the future - convert everything from charge controller and poe log to UTC and then convert based on local time...
    timeZones = []
    myTimeZone = getSysInfo("localhost",'tz')
    # print("My TZ: ", myTimeZone)

    sysC = []
    sysCity = []

    # dstIP = dstIP[0:1]

    #iterate through each device
    for i in dstIP:
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

        try:
            tempCity = getSysInfo(i,'city')
        except:
            tempCity = " "
        
        if type(tempCity) == type(None) or tempCity == '':
            tempCity =  " "
        sysCity.append(tempCity)

    # print(timeZones)

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # print("server names", len(server_names))

    print("sysCity:")
    print(sysCity)
    # go over ccData for each server
    for i, item in enumerate(ccData):
        print("SERVER:", server_names[i])
        #draw sun data for each server
        draw_ring(item,i+start_radius_data+1, energyParam,timeZones[i], myTimeZone)
        # print name of each server
        text_curve(i+start_radius_data, "SERVER:"+server_names[i]+"-"+sysCity[i], 0, 18, 18, ring_rad)
        
    print('completed enumerate server data loop')
    
    #Draw Active Server Rings
    sortPOE(log, timeZones, myTimeZone)
    # print("dfPOE.shape", dfPOE.shape)
    # print(dfPOE)

    # draw_server_arc(0, 0, Pi, (1,0,0))
    drawPOEKey(sysC)

    if dfPOE.shape[1] > 0:
        #for l, item in enumerate(dfPOE.shape[0]):
        for l in range(dfPOE.shape[0]):
            if l == 0:
                # print("Server:" ,sysC[dfPOE['device'].iloc[l]])
                # print( sysC[dfPOE['device'].iloc[l]])
                # print("First Angle:", dfPOE['angle'].iloc[l])
                draw_server_arc(dfPOE['device'].iloc[l]+start_radius_data+0.1, 2*Pi, dfPOE['angle'].iloc[l]*(Pi/180), sysC[dfPOE['device'].iloc[l]])
            else:
                # print( sysC[dfPOE['device'].iloc[l]])
                # print("Server:" ,sysC[dfPOE['device'].iloc[l]])
                # print("ring:", dfPOE['device'].iloc[l])
                # print("start arc:", dfPOE['angle'].iloc[l])
                # print("stop arc:", dfPOE['angle'].iloc[l-1])
                draw_server_arc(dfPOE['device'].iloc[l]+start_radius_data+0.1, dfPOE['angle'].iloc[l-1]*Pi/180, dfPOE['angle'].iloc[l]*Pi/180, sysC[dfPOE['device'].iloc[l]])

    print("sysC:")
    print(sysC)
    
    #lines(interval in house, stroke weight, opacity)
    lines(2, 1, 0.2)
    lines(12, 1.5, 1)
    
    circles(1.5, 1)

    # Now export the surface
    surface.get_npimage() # returns a (width x height x 3) numpy array
    surface.write_to_png(path+'/createHTML/viz-assets/clock.png')

    background = Image.open(path+'/createHTML/viz-assets/2023-clock.png')
    foreground = Image.open(path+'/createHTML/viz-assets/clock.png')
    
    mask = Image.open(path+'/createHTML/viz-assets/mask7.png').resize(background.size).convert('L')
    background.paste(foreground, (0, 0), mask)

    #this image goes to the frontend/images directory
    background.save(imgDST + "/clock.png")

    exhibitionbackground = Image.open(path+'/createHTML/viz-assets/2023-clock-1.png')
    exhibitionforeground = Image.open(path+'/createHTML/viz-assets/clock-e.png')
    
    #this image goes to the frontend/images directory

    exhibitionbackground.paste(exhibitionforeground, (0, 0), mask)
    exhibitionbackground.save(imgDST+"/clock-exhibit.png")

   
    # alphaBlended2 = Image.blend(foreground, background, alpha=.5)
    # alphaBlended2.save("clock1.png")
    #archive images
    # archiveImage = Image.open(imgDST+"/clock.png")
    # archiveImage.save('viz-archive/clock-' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +'.png') #archive plot


if __name__ == "__main__":

    main()
