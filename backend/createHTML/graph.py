# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 
from textwrap import wrap

hours = 72
server_labels=["Gilgamesh Zone", "Newcastle", "Van Brunt"]
server_labels = [ '\n'.join(wrap(l, 10)) for l in server_labels ]
# Declaring a figure "gnt" 
fig, gnt = plt.subplots() 

fig.set_figheight(4.5)
fig.set_figwidth(9)
# Setting Y-axis limits 
gnt.set_ylim(0, 30) 




# Setting X-axis limits 
gnt.set_xlim(0, 72) 

# Setting labels for x-axis and y-axis 

gnt.set_ylabel('Server') 

#gnt.xaxis.set_rotate_label(False)  # disable automatic rotation
gnt.set_xlabel('Hours ago', rotation=180)


# Setting ticks on y-axis 
gnt.set_yticks([5, 15, 25]) 
# Labelling tickes of y-axis 
gnt.set_yticklabels(server_labels) 


# Setting graph attribute 
gnt.grid(True) 

# You can specify a rotation for the tick labels in degrees or with keywords.
for tick in gnt.get_xticklabels():
     tick.set_rotation(90)

     # You can specify a rotation for the tick labels in degrees or with keywords.
for tick in gnt.get_yticklabels():
     tick.set_rotation(180)


# Declaring a bar in schedule 
for x in range(hours):
    a=x/72
    #print(a)
    gnt.broken_barh([(x, 1)], (21, 8), facecolors =(1, 0.84, 0.0, a))
gnt.broken_barh([(0, 24)], (22, 6), facecolors =('#0f0f0f')) 

  
# Declaring multiple bars in at same level and same width 
for x in range(hours):
    a=1-x/72
    #print(a)
    gnt.broken_barh([(x, 1)], (1, 8), facecolors =(1, 0.84, 0.0, a))
gnt.broken_barh([(24, 24), (54, 6)], (2, 6), 
                         facecolors ='#0f0f0f') 
  
for x in range(hours):
    a=1-x/72
    #print(a)
    gnt.broken_barh([(x, 1)], (11, 8), facecolors =(1, 0.84, 0.0, a))
gnt.broken_barh([(48, 6), (60, 12), (130, 10)], (12, 6), 
                                  facecolors =('#0f0f0f')) 

#spacing around graph
plt.gcf().subplots_adjust(bottom=0.10)
plt.gcf().subplots_adjust(left=0.10)

#plt.savefig("test.svg")

plt.savefig("../../../../web-2/images/gantt1.png", transparent=True) 