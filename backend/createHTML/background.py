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

#Global variables

W = 1500
H = 1500

#Run settings
LOCAL = 1
DEBUG_MODE = 0

PATH = "/home/pi/solar-protocol"
if LOCAL == 1:
    PATH = ".."   

DEVICE_LIST = PATH + "/api/v1/deviceList.json"

HOURS = 72
HOUR_ANGLE =(2*math.pi)/72 #angle of an hour
RING_RAD = 61
RING_START_POSITION = 1
DAYS = (HOURS/24)+1


###

    


def draw_circles(surface):
    diameter = 1224
    radius = diameter/2
    #tick length
    big_tick_len = 35
    med_tick_len = 20
    sml_tick_len = 5
    label_interval=4; #label interval (hours)
    tick = 1
    subtick = 0.1
    vert_text = 25
    label_angle=(360/HOURS*(math.pi/180))
    #label_angle=(360/(HOURS/label_interval))*(math.pi/180)
    tick_angle = (360/HOURS)*math.pi/180
    subtick_angle = (360/(HOURS/subtick))*math.pi/180


    #draw circles
    circ = g.circle(r=radius, xy=(W/2, H/2), stroke_width=4, stroke=(1,1,1))
    circ.draw(surface)
    #for loop through each server *******
    for i in range(10):
        inner_circ = g.circle(r=(radius/10)*i, xy=(W/2, H/2), stroke_width=1, stroke=(1,1,1))
        inner_circ.draw(surface)
    #draw outer labels for tick marks
    for i in range(HOURS):
        if i % label_interval == 0:
            angle= -1*(label_angle*i)
            text = g.text(str(i) + " hrs", fontfamily='serif',  fontsize=20, fill=(1,1,1), xy=(W/2, H/2-radius-vert_text))
            text_translated = text.rotate(angle, center=[W/2,H/2])
            text_translated.draw(surface)

    #draw tick marks
    for i in range(72):
        if i % tick == 0:
            angle= -1*(tick_angle*i)
            tick_line=g.polyline(points=[(0,-radius), (0, -radius+med_tick_len)], stroke_width=1,
                     stroke=(255), fill=(255))
            #tick_translated = text.translate(xy=[W/2, H/2])
            tick_translated = tick_line.rotate(tick_angle, center=[W/2,H/2])
            tick_translated.draw(surface)

    # #draw subtick marks
    # for i in range(72):
    #     if i % subtick == 0:
    #         subtick_line=g.polyline(points=[(0,-r), (0, -r+sml_tick_len)], stroke_width=1,
    #                  stroke=(255), fill=(255))
    #         subtick_translated = text.rotate(-subtick_angle, center=[W/2,H/2])
    #         #subtick_translated.draw(surface)

#line 119, arrow, check the thing below.
    arc = g.arc(r=radius+540, a1=-math.pi/2-0.9, a2=-math.pi/2-0.425, fill=(1,1,1))
    surface.write_to_png("circles.png")



# -------------- PROGRAM --------------------------------------------------------------------------------
def main():
    surface = g.Surface(width=W,height=H)
    draw_circles(surface)
    # square = g.square(l=20, fill=(1,0,0), xy=(40,40))
    # circle = g.circle(r=20, fill=(1,2,0), xy=(50,30))
    # group_1 = g.Group([square, circle])
    # group_2 = group_1.translate(xy=[30,30]).rotate(math.pi/4)
    # group_3 = g.Group([circle, group_2])

    

    # group_1.draw(surface)
    # group_2.draw(surface)
    # group_3.draw(surface)
    # surface.write_to_png("my_masterwork.png")



if __name__ == "__main__":
    main()
