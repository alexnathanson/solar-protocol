
import gizeh as g
import math

w = 500
h = 500

Pi = 3.14159
hours = 72
ah = (2*Pi)/hours #angle of an hour
ring_rad = 20

server_names = ["Server 1", "Server 2"]

# initialize surface
surface = g.Surface(width=w, height=h) # in pixels

text = g.text("Hello World", fontfamily="Georgia",  fontsize=10, fill=(0,0,0), xy=(100,100), angle=Pi/12)
text.draw(surface)

# draw_sun(ring number, x loc, y loc, stroke weight, _hour, _alpha)
def draw_sun(server_no, cx, cy, sw, hour, alpha):
    a = -Pi/2 - (hour*ah)
    arc = g.arc(r = server_no*ring_rad, xy = [cx, cy], a1 = a, a2 = a+ah , stroke=(0, 0, 1, alpha), stroke_width= sw)
    arc.draw(surface)

#def draw_server_arc(server_no, startAngle, stopAngle, color):
def draw_server_arc(server_no, start, stop, c):
  # Start in the center and draw the circle
    circle = g.arc(r=server_no*ring_rad, xy = [250, 250], a1 = stop-Pi/2, a2 = start-Pi/2  , stroke=c, stroke_width= 1.5)
    circle.draw(surface)  

def text_curve(cr, message, angle, spacing, ts):

  # Start in the center and draw the circle
    circle = g.circle(r=cr, xy = [250, 250], stroke=(1,1,1), stroke_width= 1.5)
    circle.draw(surface)
    # We must keep track of our position along the curve
    arclength = 0
    # For every letter
    for i in range(len(message)):
        currentChar = message[i]
        print(message[i])
        # guessing the width of each char
        spacing = 15

        # Each box is centered so we move half the width
        arclength = arclength + spacing/2
        print("arclength")
        print(arclength)
        # Angle in radians is the arclength divided by the radius
        # Starting on the left side of the circle by adding PI
        theta = (-1/2*Pi) + arclength / cr + angle  
        print("theta")
        print(theta)
        # Polar to cartesian coordinate conversion
        # add 250 so that the origin translates to center of screen, then add coords
        x = 250 + cr * math.cos(theta)
        y = 250 + cr * math.sin(theta)
        # Rotate the box
        # rotate(theta+PI/2)   # rotation is offset by 90 degrees
        # Display the character
        # fill(0)
        # text(currentChar,0,0)
        text = g.text(message[i], fontfamily="Georgia",  fontsize=ts, fill=(0,0,0), xy = [x, y])
        text = text.rotate(theta+(Pi/2), center=[x,y]) # rotation around a center
        text.draw(surface)
        # popMatrix()
        # Move halfway again
        arclength += spacing/2

    

draw_sun(4, w/2, h/2, 20, 0, 0.1) 
draw_sun(4, w/2, h/2, 20, 1, 0.5) 
draw_sun(4, w/2, h/2, 20, 2, 1) 

#def text_curve(cr, message, angle, spacing, ts):
text_curve(100, "Server 1", 0, 15, 20)

draw_server_arc(2, 0, 3*Pi/2, (1,0,0))

# Now export the surface
surface.get_npimage() # returns a (width x height x 3) numpy array
surface.write_to_png("circle.png")
