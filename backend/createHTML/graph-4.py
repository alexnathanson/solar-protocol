import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from random import choice
from PIL import Image
import pandas as pd
from glob import glob

#global variables
days = 4 # how many days do you want?
hours = 72
tick_interval = 2
label_interval = 12
sun_color = ['00','26','66','B3']
owd = os.getcwd()
csv_paths = '../../charge-controller/data/*.csv'

#get sun data files and order according to date
#BUT THIS IS GETTING WRITE DATE AND NOT NAME DATE <<<<<<< 
files = sorted(glob(csv_paths))

recent_files= files[-days:]
#print("Most recent files: "+files[0:3])
print(recent_files)


#combine last 4 file
df_from_each_file = (pd.read_csv(f, sep=',', encoding='latin-1') for f in recent_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df = df_merged


df['datetime'] = df['datetime'].astype(str) #convert entire "Dates" Column to string 
df['datetime']=pd.to_datetime(df['datetime']) #convert entire "Dates" Column to datetime format this time 
df.index=df['datetime'] #replace index with entire "Dates" Column to work with groupby function
df_hours = df.groupby(pd.Grouper(freq='H')).mean() #take daily average of multiple values
df_hours = df_hours.tail(72) # last 72 hours
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df_hours["PV current"])
    

#average_solar(df_merged)

#get last 72 values for solarCurrent in df_merged and use in viz.
# do i look at datetime or just the last 72?


oldest = files[0]
newest = files[-1]

#print ("Newest:" +newest)


# STYLE COLORS
# radar grid white solid grid lines

plt.rc('grid', color='#6b6b6b', linewidth=0.3, linestyle='-')

# label colors
plt.rc('xtick', labelsize=6, color="#e0e0e0")
plt.rc('ytick', labelsize=10, color="none")


#customize inside labels
server_names = ("Brooklyn", "Canada", "Dominica", "Newcastle", "", "")
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
#plt.xticks(ticks, x_labels)
plt.xticks(ticks)
plt.yticks(np.arange(3,10))
#label.set_visible(False)

for label in ax.get_xticklabels()[::1]: #only show every second label
#     # if(n==0):
#     #     label.set_rotation(np.pi)
#     #     n=1
#     # else:
#     #     label.set_rotation(0)
    label.set_visible(False)



# for i, label in enumerate(ax.get_xticklabels()):
#     label.set_rotation(i*90)





#arcs
def draw_sun(server_no, start, stop, alpha):
     for i in range(start, stop, 1):
        #ax.bar(rotation, arc cell length, width of each cell, width of each arc , radius of bottom, color, edgecolor )(1, 0.84, 0.0, alpha) '#D4AF37'+alpha
        ax.bar((rotation*np.pi/180)+(i * 2 * np.pi / hours), 0.8, width=2 * np.pi / hours, bottom=server_no+0.1,color=(1, 0.85, 0, alpha), edgecolor = "none")

def draw_server_arc(server_no, start, stop, c):
    for i in range(start, stop, 1):
        ax.bar((rotation*np.pi/180)+(i * 2 * np.pi / hours), 0.33, width=2 * np.pi / hours, bottom=server_no+0.33,color=c, edgecolor = c)


#ax.set_yticks([])
plt.ylim(0,10) #puts space in the center (start of y axis)

df_hours["PV current"] = df_hours["PV current"] / df_hours["PV current"].max()

# #correlate sun data wtih colors 
for i, current in enumerate(df_hours["PV current"].tolist()):
   # print(current)

    draw_sun(5, i, i+2, current)
    draw_sun(4, i, i+2, current)
    draw_sun(3, i, i+2, current)



# for i in range(72):  
    

    # draw_sun(3, i, i+2, sun_color[(i+2)%4])
    # draw_sun(4, i, i+2, sun_color[(i+3)%4])
    # draw_sun(5, i, i+2, sun_color[(i+1)%4])

sc = "white"

# draw_server_arc(2, 3, 7, sc)
# draw_server_arc(3, 7, 10, sc)
# draw_server_arc(2, 10, 15, sc)
# draw_server_arc(4, 15, 24, sc)
draw_server_arc(5, 24, 30, sc)
draw_server_arc(2, 30, 35, sc)
draw_server_arc(3, 35, 55, sc)
draw_server_arc(5, 55, 72, sc)


#add line for now
#ax.plot(wind_speed, wind_direction, c = bar_colors, zorder = 3)
ax.plot((0,0), (0,10), color="white", linewidth=0.3, zorder=10)
os.chdir(owd)
bg = Image.open('background-Arial.png')


#plt.show()
plt.savefig('clock.png')
fg=Image.open('clock.png')
bg.paste(fg, (0,0), fg)
bg.save('final-Arial.png')