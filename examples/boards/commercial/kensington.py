"""
A "Kensington" board example for protograf

Written by: Derek Hohls
Created on: 22 January 2026
"""
from protograf import *

# set the colors
page_fill = "black"
outline = "green"
red = "#E8445C"
blue = "#5D80EA"

Create(filename="kensington.pdf", margin=0.25, paper="A4", fill=page_fill)
# Blueprint(stroke_width=0.5, fill="black")

def grouping(x=0, y=0, filled=None):
    # draw outer 12-sided polygon
    outer = Polygon(
        cx=x, cy=y,
        side=1, sides=12, fill=None, stroke=outline)
    # draw inner 6-sided polygon
    if filled:
        inner = Polygon(
            cx=x, cy=y,
            side=1, sides=6,
            fill=filled, stroke=outline)
    else:
        inner = Polygon(
            cx=x, cy=y,
            side=1, sides=6,
            fill=None, stroke=outline)
        Polygon(
            cx=x, cy=y,
            side=0.9, sides=6,
            fill=None, stroke="white", stroke_width=3)
    # connect vertices of outer polygon to those of inner polygon
    for point in range(1, 7):
        Line(connections=[
                (outer, 'v', point * 2 - 1), (inner, 'v', point), (outer, 'v', point * 2)
            ],
            stroke=outline)

# draw the 6 sets of shapes
grouping(x=2, y=4, filled=red)
grouping(x=4.365, y=2.635)

Save()
