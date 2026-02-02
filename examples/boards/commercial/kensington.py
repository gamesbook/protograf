"""
A "Kensington" board example for protograf

Written by: Derek Hohls
Created on: 22 January 2026
"""
from protograf import *

# set the colors
page_fill = "black"
GREEN = "green"
RED = "#E8445C"
BLUE = "#5D80EA"

Create(filename="kensington.pdf", margin=0.25, paper="A4", fill=page_fill)

SIDE = 2  # length of the side of a colored hexagon
X = 10  # x-position for centre of central hexagon
Y = 14.5  # y-position for centre of central hexagon

def grouping(x=0, y=0, filled=None):
    # draw outer 12-sided polygon
    outer = Polygon(
        cx=x, cy=y,
        side=SIDE, sides=12, fill=None, stroke=GREEN)
    # draw inner 6-sided polygon
    if filled:
        inner = Polygon(
            cx=x, cy=y,
            side=SIDE, sides=6,
            fill=filled,
            stroke=GREEN)
    else:
        inner = Polygon(
            cx=x, cy=y,
            side=SIDE, sides=6,
            fill=None,
            stroke=GREEN)
        Polygon(
            cx=x, cy=y,
            side=0.9*SIDE, sides=6,
            fill=None,
            stroke="white", stroke_width=3)
    # connect vertices of outer polygon to those of inner polygon
    for point in range(1, 7):
        Line(connections=[
                (outer, 'v', point * 2 - 1),
                (inner, 'v', point),
                (outer, 'v', point * 2)
            ],
            stroke=GREEN)


HEIGHT = SIDE * sqrt(3)  # edge-to-edge across hexagon
LENGTH = HEIGHT + SIDE  # distance between hexagon centres

grouping(x=X, y=Y)  # central set
settings = [
    (BLUE, -30), (None, -90), (RED, -150), (RED, -210), (None, -270), (BLUE, -330),]
for setting in settings:
    hexx = point_from_angle(Point(X, Y), LENGTH, setting[1])
    grouping(x=hexx.x, y=hexx.y, filled=setting[0])

Text("Kensington", stroke=RED, x=4, y=23.7,
     font_name="Times New Roman", font_size=36)
Text("Kensington", stroke=BLUE, x=15.7, y=5.3,
     font_name="Times New Roman", font_size=36,
     rotation=180)

Save()
