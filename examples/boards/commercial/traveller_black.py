"""
A Traveller RPG map example for protograf

Written by: Derek Hohls
Created on: 2 March 2024
Notes:
    * Black style; 'A' sector
"""

from protograf import *

Create(filename="traveller_black.pdf", margin=0.25, paper=A4)

# set colors
map_fill = black
hex_lines = lightgrey
map_border = lightgrey

Rectangle(x=0.0, y=-0.05, width=20, height=29.2, stroke=map_fill, fill=map_fill)

Hexagons(
    rows=10,
    cols=8,
    side=1.6,
    y=0.0,
    x=0.0,
    hex_offset="odd",
    coord_elevation="t",
    coord_offset=0,
    coord_font_size=11,
    coord_stroke=hex_lines,
    coord_padding=2,
    coord_start_x=9,
    fill=map_fill,
    stroke=hex_lines,
)

# Map "edge" lines
Line(x=0.4, y=-0.05, x1=0.4, y1=29.05, stroke=map_border, stroke_width=3)
Line(x=19.6, y=-0.05, x1=19.6, y1=29.05, stroke=map_border, stroke_width=3)
Line(x=0.4, y=1.4, x1=19.6, y1=1.4, stroke=map_border, stroke_width=3)
Line(x=0.4, y=29.05, x1=19.6, y1=29.05, stroke=map_border, stroke_width=3)

# Tidy bottom edge
Rectangle(x=-0.2, y=-1.05, width=20.5, height=1.2, stroke=white, fill=white)

Save()
