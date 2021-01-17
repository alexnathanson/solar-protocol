
import matplotlib.pyplot as plt
import math 



# Compute pie slices
def plot_ring(no, center, color):
    theta = center*math.pi/180 #angle in radians
    radii = 0.1
    width = 0.5
    colors = color

    ax = plt.subplot(111, projection='polar')
    ax.bar(theta, radii, width=width, bottom=no, color=colors, alpha=0.5)


plot_ring(1, 0, "blue")
plot_ring(2, 0, "yellow")
plt.show()
