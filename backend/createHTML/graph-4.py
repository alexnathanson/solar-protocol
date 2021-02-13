import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import requests
from random import choice
from PIL import Image
import pandas as pd
from glob import glob
import json

#global variables
days = 4 # get 4 days of csv files so we know we definitely get 72 hours of data
hours = 72
tick_interval = 2
label_interval = 12
sun_color = ['00','26','66','B3']
owd = os.getcwd()

# TO DO
# import data using API from each server on the network
# do we need to deal with time zones? Or can the API just return the last 72 hours of data?
# write algorithm for turning the list of timestamps for the active server into a form that can use the drawServerarc();

deviceList = "/home/pi/solar-protocol/backend/api/v1/deviceList.json";

def getDeviceInfo(getKey):

    ipList = []

    with open(deviceList) as f:
      data = json.load(f)

    #print(data)

    for i in range(len(data)):
        ipList.append(data[i][getKey])

    return ipList

def getIt(dst,ccValue):
    print("GET from " + dst)
    try:
        x = requests.get('http://' + dst + "/api/v1/chargecontroller.php?value="+ccValue + "&duration=4",timeout=5)
        #print(json.loads(x.text))
        return json.loads(x.text)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

#drawing the sunshine data (yellow)
def draw_ring(ccDict, ring_number, energy_parameter):

    ccDataframe = pd.DataFrame.from_dict(ccDict, orient="index")

    ccDataframe.columns = ccDataframe.iloc[0]
    ccDataframe = ccDataframe.drop(ccDataframe.index[0])
    #ccDataframe['datetime']=ccDataframe.index
    ccDataframe = ccDataframe.reset_index()
    ccDataframe.columns = ['datetime',energy_parameter]
    #ccDataframe.index.names = ['datetime']
    print(ccDataframe.head())

    ccDataframe['datetime'] = ccDataframe['datetime'].astype(str) #convert entire "Dates" Column to string 
    ccDataframe['datetime']=pd.to_datetime(ccDataframe['datetime']) #convert entire "Dates" Column to datetime format this time 
    ccDataframe[energy_parameter] = ccDataframe[energy_parameter].astype(float) #convert entire column to float
    ccDataframe.index=ccDataframe['datetime'] #replace index with entire "Dates" Column to work with groupby function
    ccDataframe = ccDataframe.drop(columns=['datetime'])
    print(ccDataframe.head())
    df_hours = ccDataframe.groupby(pd.Grouper(freq='H')).mean() #take hourly average of multiple values
    #df_hours = ccDataframe.set_index('datetime').groupby(pd.Grouper(freq='H')).mean() #take hourly average of multiple values
    df_hours = df_hours.tail(72) # last 72 hours
    #print(df_hours[energy_parameter])
    # oldest1 = files1[0]
    # newest1 = files1[-1]
    df_hours[energy_parameter] = df_hours[energy_parameter] / df_hours[energy_parameter].max()

    # #correlate sun data wtih colors 
    for i, current in enumerate(df_hours[energy_parameter].tolist()):
        # print(current)
        draw_sun(ring_number, i, i+2, current)


    return df_hours
#gold: color=(1, 0.85, 0, alpha)

#arcs
def draw_sun(server_no, start, stop, alpha):
     for i in range(start, stop, 1):
        #ax.bar(rotation, arc cell length, width of each cell, width of each arc , radius of bottom, color, edgecolor )(1, 0.84, 0.0, alpha) '#D4AF37'+alpha
        ax.bar((rotation*np.pi/180)+(i * 2 * np.pi / hours), 1, width=2 * np.pi / hours, bottom=server_no+0.1, color=(1, 0.85, 0, alpha), edgecolor = "none")


def draw_server_arc(server_no, start, stop, c):
    for i in range(start, stop, 1):
        ax.bar((rotation*np.pi/180)+(i * 2 * np.pi / hours), 0.33, width=2 * np.pi / hours, bottom=server_no+0.45, color=c, edgecolor = c)


dstIP = getDeviceInfo('ip')
energyParam = "PV-current"
ccData = []
for i in dstIP:
    #print(i)
    ccData.append(getIt(i,energyParam))

pd.set_option("display.max_rows", None, "display.max_columns", None)

# STYLE COLORS
# radar grid white solid grid lines

plt.rc('grid', color='#6b6b6b', linewidth=0.3, linestyle='-')

# label colors
plt.rc('xtick', labelsize=6, color="#e0e0e0")
plt.rc('ytick', labelsize=10, color="none")


#customize inside labels
server_names = getDeviceInfo('name')

# for label in ax.get_yticklabels()[::]: #only show every second label
#     label.set_visible(False)

# set up graph
fig = plt.figure(figsize=(15, 15)) #SIZE
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, facecolor='none')

# ax.set_rticks(server_names)  # Less radial ticks
# ax.set_rlabel_position(-22.5)  # Move radial labels 

#ax.spines['polar'].set_visible(True) #turn off outside border
ax.spines['polar'].set_color('#6b6b6b')

#background color
fig.set_facecolor('none') 

# AXIS PROPERTIES
ax.set_theta_direction(-1)

ax.set_theta_offset(np.pi/2.0)

rotation=360/hours/2
#print(rotation)

n=0
#customize outside labels
ticks = np.arange(hours/tick_interval)*2*np.pi/(hours/tick_interval)
x_labels = list(range(0,int(hours), tick_interval))
x_labels[0]="Now"

plt.xticks(ticks)
plt.yticks(np.arange(3,10))


for label in ax.get_xticklabels()[::1]: #only show every second label
    label.set_visible(False)



# for i, label in enumerate(ax.get_xticklabels()):
#     label.set_rotation(i*90)


plt.ylim(0,10) #puts space in the center (start of y axis)

#Draw Sun Data for each server
#draw_ring(data, ringNo, parameter);
for rPV in range(len(ccData)):
    draw_ring(ccData[rPV],rPV, energyParam)
# draw_ring(csv_paths2, 4, "PV current")
# draw_ring(csv_paths3, 5, "PV current")
# draw_ring(csv_paths2, 6, "PV current")
# draw_ring(csv_paths1, 7, "PV current")


#Draw Active Server Rings

sc = "white"
#draw_server_arc(ringNo, startHour, stopHour, color )
draw_server_arc(3, 35, 55,  '#00158a')
draw_server_arc(4, 30, 35, "pink")
draw_server_arc(5, 55, 72, sc)
draw_server_arc(5, 24, 30, 'green')


#add line for now
#ax.plot(wind_speed, wind_direction, c = bar_colors, zorder = 3)
ax.plot((0,0), (0,10), color="white", linewidth=0.3, zorder=10)
os.chdir(owd)


plt.savefig('clock.png') #save plot


background = Image.open("face-6-server-days.png")
foreground = Image.open("clock.png")
Image.alpha_composite(foreground, background).save("result.png")