import gizeh as g
import datetime
from dateutil.relativedelta import relativedelta
import csv
from json.decoder import JSONDecodeError
import requests, json


def read_csv():
    filename = "../../charge-controller/data/tracerData2021-03-15.csv"
    # filename = (
    #     "../../charge-controller/data/tracerData" + str(datetime.date.today()) + ".csv"
    # )
    with open(filename, "r") as data:
        alllines = [line for line in csv.DictReader(data)]

    # line = alllines[-1]
    # line["PV voltage"] = float(line["PV voltage"])
    # line["PV current"] = float(line["PV current"])
    # line["PV power L"] = float(line["PV power L"])
    # line["PV power H"] = float(line["PV power H"])
    # line["battery voltage"] = float(line["battery voltage"])
    # line["battery current"] = float(line["battery current"])
    # line["battery power L"] = float(line["battery power L"])
    # line["battery power H"] = float(line["battery power H"])
    # line["load voltage"] = float(line["load voltage"])
    # line["load current"] = float(line["load current"])
    # line["load power"] = float(line["load power"])
    # line["battery percentage"] = float(line["battery percentage"])
    return alllines


def get_weather():
    complete_url = "http://api.openweathermap.org/data/2.5/weather?lon=-74&lat=40.68&appid=24df3e6ca023273cd426f67e7ac06ac9"

    print(complete_url)

    response = requests.get(complete_url)
    x = response.json()
    y = x["main"]
    current_temperature = y["temp"]
    current_humidiy = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"]

    sunrise = datetime.datetime.fromtimestamp(x["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(x["sys"]["sunset"])
    sunrise = sunrise.strftime("%I:%M %p")
    sunset = sunset.strftime("%I:%M %p")
    return (sunrise, sunset)


def remap(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


def sunrise_sunset(
    surface, x_padding_left, x_padding_right, w, t, y, tick_width, now_length
):
    sunrise, sunset = get_weather()
    t_tick_length = t
    print("sunset", sunset)
    print("sunrise", sunrise)

    sr = datetime.datetime.strptime(sunrise, "%I:%M %p")
    sunrise = datetime.datetime.strftime(sr, "%H:%M")

    sr_seconds = sr.hour * 3600 + sr.minute * 60
    total_seconds = 24 * 60 * 60
    print("sr_seconds:", sr_seconds)
    x_sunrise = remap(sr_seconds, 0, total_seconds, x_padding_left, w - x_padding_right)

    ss = datetime.datetime.strptime(sunset, "%I:%M %p")
    sunset = datetime.datetime.strftime(ss, "%H:%M")
    ss_seconds = (ss.hour) * 3600 + ss.minute * 60
    print("ss_seconds:", ss_seconds)
    print("total_seconds", total_seconds)
    x_sunset = remap(ss_seconds, 0, total_seconds, x_padding_left, w - x_padding_right)

    time_now = datetime.datetime.now()
    print("time_now:", time_now)
    now_seconds = (time_now.hour) * 3600 + time_now.minute * 60 + time_now.second
    x_now = remap(now_seconds, 0, total_seconds, x_padding_left, w - x_padding_right)
    print("x_now:", x_now)

    tick4 = g.polyline(
        points=[(x_sunrise, y), (x_sunrise, (y - t_tick_length))],
        stroke_width=tick_width,
    )
    tick4.draw(surface)

    sr_text = g.text(
        "Sunrise: " + str(sunrise),
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_sunrise, (y - t_tick_length - 8)],
    )
    sr_text.draw(surface)
    tick5 = g.polyline(
        points=[(x_sunset, y), (x_sunset, (y - t_tick_length))], stroke_width=tick_width
    )
    tick5.draw(surface)
    ss_text = g.text(
        "Sunset: " + str(sunset),
        fontfamily="Arial",
        fontsize=12,
        h_align="center",
        xy=[x_sunset, (y - t_tick_length - 8)],
    )
    ss_text.draw(surface)
    # time now
    tick6 = g.polyline(
        points=[(x_now, y), (x_now, (y - t_tick_length - now_length))],
        stroke_width=tick_width,
    )
    tick6.draw(surface)
    c6 = g.circle(r=5, xy=[x_now, (y - t_tick_length - now_length)], fill=(0, 0, 0))
    c6.draw(surface)
    now_text = g.text(
        "Time Now",
        fontfamily="Arial",
        fontsize=12,
        h_align="center",
        xy=[x_now, (y - t_tick_length - now_length - 15)],
    )
    now_text.draw(surface)

    line6 = g.polyline(
        points=[(x_now, y - 4), (w - x_padding_right, y - 4)], stroke_width=8
    )
    line6.draw(surface)


def y_axis_text(
    surface,
    w,
    h,
    units,
    y_axis_min,
    y_axis_max,
    x_padding_right,
    y_padding_top,
    y_padding_bottom,
):
    min_text = g.text(
        str(y_axis_min) + units,
        fontfamily="Arial",
        fontsize=12,
        h_align="left",
        xy=[w - x_padding_right + 3, (h - y_padding_bottom)],
    )
    min_text.draw(surface)
    max_text = g.text(
        str(y_axis_max) + units,
        fontfamily="Arial",
        fontsize=12,
        h_align="left",
        xy=[w - x_padding_right + 3, (y_padding_top)],
    )
    max_text.draw(surface)


def draw_graph(surface, data, label, w, h, y_axis_min, y_axis_max, units):

    # AXIS
    x_padding_left = 50
    x_padding_right = 50
    y_padding_bottom = 50
    y_padding_top = 5

    # in case you want the y axis to have negative values
    zero_y = remap(0, y_axis_min, y_axis_max, h - y_padding_bottom, y_padding_top)

    axisy = g.polyline(
        points=[
            (w - x_padding_right - 1, 0 + y_padding_top),
            (w - x_padding_right - 1, h - y_padding_bottom),
        ],
        stroke_width=2,
        stroke=(0, 0, 0),
        fill=(0, 0, 0),
    )
    axisx = g.polyline(
        points=[(x_padding_left, zero_y), (w - x_padding_right, zero_y)],
        stroke_width=2,
        stroke=(0, 0, 0),
        fill=(0, 0, 0),
    )

    axisy.draw(surface)
    axisx.draw(surface)

    # DATA
    px = 0
    py = 0
    for index, line in enumerate(data):

        x_axis_len = w - (x_padding_left + x_padding_right)
        # space = x_axis_len/(len(data)+1)

        # DRAW DATA POINTS
        valy = float(line[label])
        date = line["datetime"]
        date = date[:-7]
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        # time stamp of datapoint in seconds
        seconds = t.hour * 3600 + t.minute * 60 + t.second
        total_seconds = 24 * 60 * 60
        print("seconds:", seconds)
        # print(val)
        dy = (
            remap(valy, y_axis_min, y_axis_max, h - y_padding_bottom, y_padding_top) - 2
        )
        dx = remap(seconds, 0, total_seconds, x_padding_left, w - x_padding_right)
        # dx = x_padding_left + (index * space)
        circle = g.circle(r=2, xy=[dx, dy], fill=(0, 0, 0))
        circle.draw(surface)

        # DRAW DATA LINE
        if index != 0:
            fit_line = g.polyline(
                points=[(previous_x, previous_y), (dx, dy)],
                stroke_width=3,
                stroke=(0, 0, 0),
                fill=(0, 0, 0),
            )
            fit_line.draw(surface)
        previous_x = dx
        previous_y = dy

        # AXIS LABELS
        # if(index%5==0):
        #     date = line["datetime"]
        #     date = date[5:-10]

        # #     x_label = g.text(date, fontfamily="Georgia",  fontsize=15, fill=(0,0,0), h_align="right", xy=[-1*(zero_y+20), dx], angle=-3.1416/2)
        # #     x_label.draw(surface)
        # x_text1 = g.text("00.00", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="left", xy=[x_padding_left+5, (zero_y+10)], angle=0)
        # x_text1.draw(surface)
        # x_text2 = g.text("N O W", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[w-(x_padding_right+5), (zero_y+10)], angle=0)
        # x_text2.draw(surface)
        # y_text1 = g.text(str(y_axis_min), fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[(x_padding_left-5), h-y_padding_bottom], angle=0)
        # y_text1.draw(surface)
        # y_text2 = g.text("0", fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[x_padding_left-5, zero_y], angle=0)
        # y_text2.draw(surface)
        # y_text3 = g.text(str(y_axis_max), fontfamily="Arial",  fontsize=10, fill=(0,0,0), h_align="right", xy=[x_padding_left-5, y_padding_top], angle=0)
        # y_text3.draw(surface)
    x_left = x_padding_left + 2
    x_middle = (w - (x_padding_left + x_padding_right)) / 2
    x_right = w - x_padding_right - 2
    y_top = h - y_padding_bottom
    y_bot = h - y_padding_bottom + 30
    y_middle = (h - (y_padding_bottom + y_padding_top)) / 2

    # draw ticks and labels
    x_text1 = g.text(
        "00.00",
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_left, y_bot + 10],
    )
    x_text1.draw(surface)
    tick1 = g.polyline(
        points=[(x_left - 1, y_bot), (x_left - 1, y_top)], stroke_width=2
    )
    tick1.draw(surface)
    x_text2 = g.text(
        "12.00",
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_middle, y_bot + 10],
    )
    x_text2.draw(surface)
    tick2 = g.polyline(points=[(x_middle, y_bot), (x_middle, y_top)], stroke_width=2)
    tick2.draw(surface)
    x_text3 = g.text(
        "24.00",
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_right, y_bot + 10],
    )
    x_text3.draw(surface)
    tick3 = g.polyline(
        points=[(x_right + 1, y_bot), (x_right + 1, y_top)], stroke_width=2
    )
    tick3.draw(surface)

    # SUNRISE SUNSET NOW
    sunrise_sunset(
        surface, x_padding_left, x_padding_right, w, 25, h - y_padding_bottom, 2, 30
    )
    y_axis_text(
        surface,
        w,
        h,
        units,
        y_axis_min,
        y_axis_max,
        x_padding_right,
        y_padding_top,
        y_padding_bottom,
    )
    # AXIS TITLES
    # y_text = g.text("PV Voltage", fontfamily="Georgia",  fontsize=20, fill=(0,0,0), xy=[-250, 25], angle=-3.1416/2)
    # y_text.draw(surface)

    # x_text = g.text("Time", fontfamily="Georgia",  fontsize=20, fill=(0,0,0), xy=[250, h-(y_padding_bottom/2)], angle=0)
    # x_text.draw(surface)

    # file_name = "/home/pi/solar-server/frontend/images/"+label+"_graph.png"
    file_name = label + "_graph.png"
    surface.write_to_png(file_name)


def draw_sun_graph(surface, data, label, w, h):
    rect = g.rectangle(lx=0, ly=0, xy=(w, h), fill=(0, 1, 1))
    rect.draw(surface)
    # AXIS
    x_padding_left = 50
    x_padding_right = 50
    y_padding_bottom = -25
    y_padding_top = 0

    # axisy = g.polyline(points=[(x_padding_left, y_padding_top), (x_padding_left, h-y_padding_bottom)], stroke_width=3, stroke=(0,0,0), fill=(0,0,0))
    axisx = g.polyline(
        points=[
            (x_padding_left, (h - (y_padding_bottom + y_padding_top)) / 2),
            (w - x_padding_right, (h - (y_padding_bottom + y_padding_top)) / 2),
        ],
        stroke_width=3,
        stroke=(0, 0, 0),
        fill=(0, 0, 0),
    )

    # axisy.draw(surface)
    axisx.draw(surface)

    av_hour = []
    average_pv = []
    average = 0
    hour = 0
    for index, line in enumerate(data):
        # print("pv voltage", line["PV voltage"])
        # get each hour
        date = line["datetime"]
        date = date[:-7]
        t1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if index == 0:
            print("index is zero")
            n = 1
            hour = t1.hour
            total = float(line["PV voltage"])
            print("first index")
            # print(type(total))
            # average_pv = total/n
            average = total / n
        else:
            if hour == t1.hour:
                # print("t1 hour", t1.hour)
                n = n + 1
                # print("n:", n)
                total = total + float(line["PV voltage"])
                # print("total:", total)
                # hour_av.append(t1.hour)
                average = total / n
                # print("average:", average_pv)
            else:
                av_hour.append(hour)
                average_pv.append(average)
                # print("t1 hour", t1.hour)
                n = 1
                total = float(line["PV voltage"])
                hour = t1.hour
                # hour_av.append(t1.hour)
                average = total / n

    av_hour.append(hour)
    average_pv.append(average)
    print(av_hour)
    print(average_pv)
    print("hours", len(av_hour))

    # draw circles
    n = 0
    limit = len(av_hour) - 1
    for i in range(0, 25):

        # for index, line in enumerate(average_pv):
        spacing = (w - (x_padding_left + x_padding_right)) / 24
        x = spacing * i
        print("circle_x", x)
        if av_hour[n] == i:
            circle_r = average_pv[n] * 0.4

            circle = g.circle(
                r=circle_r,
                xy=[x_padding_left + x, (h - (y_padding_bottom + y_padding_top)) / 2],
                stroke_width=3,
                fill=(0, 0, 0),
            )
            circle.draw(surface)
            if n < limit:
                n = n + 1
        else:
            print("nodata")

    x_left = x_padding_left
    x_middle = (w - (x_padding_left + x_padding_right)) / 2
    x_right = w - x_padding_right
    tick_width = 2
    b_tick_length = 15
    y_middle = (h - (y_padding_bottom + y_padding_top)) / 2
    # draw bottom ticks and labels
    x_text1 = g.text(
        "00.00",
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_left, (y_middle - 15 - 5)],
        angle=0,
    )
    x_text1.draw(surface)
    tick1 = g.polyline(
        points=[(x_left + 1, y_middle), (x_left + 1, y_middle - 15)],
        stroke_width=tick_width,
    )
    tick1.draw(surface)
    # x_text2 = g.text("12.00", fontfamily="Arial",  fontsize=12 , fill=(0,0,0), h_align="center", xy=[x_middle, b_tick_length+5+(h-(y_padding_bottom+y_padding_top))/2], angle=0)
    # x_text2.draw(surface)
    # tick2 = g.polyline(points=[(x_middle, b_tick_length+(h-(y_padding_bottom+y_padding_top))/2), (x_middle, (h-(y_padding_bottom+y_padding_top))/2)], stroke_width=tick_width)
    # tick2.draw(surface)
    x_text3 = g.text(
        "24.00",
        fontfamily="Arial",
        fontsize=12,
        fill=(0, 0, 0),
        h_align="center",
        xy=[x_right, (y_middle - 15 - 5)],
        angle=0,
    )
    x_text3.draw(surface)
    tick3 = g.polyline(
        points=[(x_right - 1, y_middle), (x_right - 1, y_middle - 15)],
        stroke_width=tick_width,
    )
    tick3.draw(surface)

    # sunrise, sunset, now
    sunrise_sunset(
        surface, x_padding_left, x_padding_right, w, 15, y_middle, tick_width, 10
    )

    # file_name = "/home/pi/solar-server/frontend/images/"+label+"_graph.png"
    file_name = label + "_graph.png"
    surface.write_to_png(file_name)


def main():
    w = 1500
    h = 300

    d = read_csv()

    # energyParam = "load voltage"
    # y_axis_min = 0
    # y_axis_max = 1
    w1 = 800
    h1 = 70
    surface1 = g.Surface(width=w, height=h)
    surface2 = g.Surface(width=w, height=h)
    surface3 = g.Surface(width=w, height=h)
    surface4 = g.Surface(width=w1, height=h1, bg_color=(1, 1, 1))
    draw_graph(surface1, d, "battery percentage", w, h, 0, 1, "%")
    draw_graph(surface2, d, "PV power L", w, h, 0, 50, "W")
    draw_graph(surface3, d, "load voltage", w, h, 0, 17.5, "V")
    draw_sun_graph(surface4, d, "PV voltage", w1, h1)


if __name__ == "__main__":
    main()
