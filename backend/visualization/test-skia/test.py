from drawbot_skia.drawbot import *
import pandas as pd
import json
import datetime
import requests
import pytz

#Run settings
local = 1
debug_mode = 1

path = "/home/pi/solar-protocol/backend"
if local == 1:
    path = "../.."   

#Global variables
deviceList = path + "/api/v1/deviceList.json"
energyParam = "PV-current"
ccData = []
days = 4 # get 4 days of csv files so we know we definitely get 72 hours of data


dfPOE = pd.DataFrame(columns = ['device', 'datetime']) 

# Get list of IP addresses that the pi can see
def getDeviceInfo(getKey):
    ipList = []

    with open(deviceList) as f:
      data = json.load(f)
    if (debug_mode):
        print("Device List data:")
        print(data)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList

#Call API for every IP address and get charge controller data 
def getCC(dst,ccValue):
    print("GET from " + dst)
    try:
        x = requests.get('http://' + dst + "/api/v1/chargecontroller.php?value="+ccValue + "&duration="+str(days),timeout=5)
        if (debug_mode):
            print("API charge controller data:")
            print(json.loads(x.text))
        return json.loads(x.text)
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
            print(json.loads(x.text))
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
def draw_ring(ccDict, ring_number, energy_parameter,timeZ):

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
    ccDataframe['timedelta'] = pd.to_timedelta(tzOffset(timeZ),'h')
    ccDataframe['datetime'] = ccDataframe['datetime'] + ccDataframe['timedelta'] 
    ccDataframe = ccDataframe.drop(columns=['timedelta'])
    
    ccDataframe[energy_parameter] = ccDataframe[energy_parameter].astype(float) #convert entire column to float
    ccDataframe.index=ccDataframe['datetime'] #replace index with entire "Dates" Column to work with groupby function
    ccDataframe = ccDataframe.drop(columns=['datetime'])
    df_hours = ccDataframe.groupby(pd.Grouper(freq='H')).mean() #take hourly average of multiple values
    df_hours = df_hours.tail(72) # last 72 hours
   
    df_hours[energy_parameter] = df_hours[energy_parameter] / df_hours[energy_parameter].max()

    # #correlate sun data wtih colors 
    for i, current in enumerate(df_hours[energy_parameter].tolist()):
        if (debug_mode):
            print("Current: ", current)
        draw_sun(ring_number, i, i+2, current) 

    return df_hours

#arcs
def draw_sun(server_no, start, stop, alpha):
     for i in range(start, stop, 1):

        #ax.bar(rotation, arc cell length, width of each cell, width of each arc , radius of bottom, color, edgecolor )(1, 0.84, 0.0, alpha) '#D4AF37'+alpha
        ax.bar((rotation*np.pi/180)+(i * 2 * np.pi / hours), 1, width=2 * np.pi / hours, bottom=server_no+0.1, color=(1, 0.85, 0, alpha), edgecolor = "none")

def draw_server_arc(server_no, start, stop, c):
    for i in range(start, stop, 1):
        ax.bar(i*(np.pi/180), 0.33, width= np.pi/180, bottom=server_no+0.45, color=c, edgecolor = c)

def sortPOE():
    global dfPOE
    print(dfPOE.head())
    for l in range(len(log)):
        tempDF = pd.DataFrame(log[l]) #convert individual POE lists to dataframe
        tempDF['datetime'] = tempDF[0]

        #tempDF['datetime'] = tempDF['datetime'].astype(str) #convert entire "Dates" Column to string 
        tempDF['datetime']=pd.to_datetime(tempDF['datetime']) #convert entire "Dates" Column to datetime format this time 
    
         #shift by TZ
        tempDF['timedelta'] = pd.to_timedelta(tzOffset(timeZones[l]),'h')
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
    print(dfPOE.shape)
    pastSeventyTwoHours = (dfPOE['datetime'] > endTime)
    dfPOE = dfPOE.loc[pastSeventyTwoHours] #filter out everything older than 3 days ago
    dfPOE = dfPOE.reset_index()
    #dfPOE = dfPOE.drop(columns=[0])

    #print(dfPOE.shape)

    dfPOE['percent']=0.0
    dfPOE['angle']=0

    if dfPOE.shape[0] > 0:
        for t in range(dfPOE.shape[0]):
            minPast = ((startTime - dfPOE['datetime'].iloc[t]).total_seconds())/60
            #print(minPast/(hours*60))
            dfPOE.at[t,'percent']= minPast/ (hours*60)
            dfPOE.at[t,'angle'] = 360-(int(dfPOE['percent'].iloc[t]*360))

    #print(dfPOE.head())
    #print(dfPOE.tail())

def tzOffset(checkTZ):
    myOffset = datetime.datetime.now(pytz.timezone(myTimeZone)).strftime('%z')
    theirOffset = datetime.datetime.now(pytz.timezone(checkTZ)).strftime('%z')
    offsetDir = 0
    if myOffset > theirOffset:
        offsetDir = 1
    else:
        offsetDir = -1 
    return offsetDir*(abs((int(myOffset)/100) - (int(theirOffset)/100)))#this only offsets to the hours... there are a few timezones in India and Nepal that are at 30 and 45 minutes


#Get IPs, using keyword ip
dstIP = getDeviceInfo('ip')

log = getDeviceInfo('log')
serverNames = getDeviceInfo('name')
print (serverNames)

#in the future - convert everything from charge controller and poe log to UTC and then convert based on local time...
timeZones = []
myTimeZone = getSysInfo("localhost",'tz')
print("My TZ: ",  myTimeZone)

sysC = []

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
        tempC = 'white'
    
    if type(tempC) == type(None) or tempC == '':
        tempC = 'white'
    sysC.append(tempC) 

print(timeZones)

pd.set_option("display.max_rows", None, "display.max_columns", None)

#customize inside labels
server_names = getDeviceInfo('name')

# set up graph using drawBot
newDrawing()
newPage(500,500)
font('georgia.ttf')
fontSize(60)


#Draw Sun Data for each server
for rPV in range(len(ccData)):
    draw_ring(ccData[rPV],rPV+2, energyParam,timeZones[rPV])




# # # set line height
# # # lineHeight(150)
# # # set font size
# # fontSize(60)
# # # draw text in a box
# # textBox("Hello World " * 10, (100, 100, 800, 800))


# rotate(5, center=(50, 50))
# text("Hello World ",(50,50))

# # fill(1, 0, 0, .5)
# fill(0,0,0,0)
# # rect(100, 100, 800, 800)
stroke(1, 0, 0, .3)
strokeWidth(10)

# # arc(center, radius, startAngle, endAngle, clockwise)
# pt1 = 238, 182
# pt2 = 46, 252
# pt0 = 74, 48

radius = 100
# path = BezierPath()
# # path.moveTo(pt0)
path.arc((250,250), radius, 0, 120, 1)

# # path.arcTo(pt1, pt2, radius)
# drawPath(path)

# saveImage("test.png")
# endDrawing()