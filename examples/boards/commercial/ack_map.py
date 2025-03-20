"""
"Adventurer Conqueror King System" map example for protograf

Written by: Derek Hohls
Created on: 3 March 2024
Notes:
"""

from protograf import *

Create(filename="ack_map.pdf", margin=0.5, paper=landscape(A3))

deepgray = "#666666"

# Header Section
Text(
    x=1.5,
    y=28,
    width=15,
    height=1,
    align="left",
    font_name="Times-Roman",
    font_size=23,
    text="ADVENTURER CONQUEROR KING",
)
Rectangle(x=15, y=27.5, width=22.5, height=1.5, stroke=darkgray, stroke_width=1.5)

# Base Map (small numbered hexes)
Hexagons(
    cols=25,
    rows=16,
    y=0,
    x=0,
    height=1.66,  # approx. two-thirds of an inch
    margin_bottom=0.25,
    margin_left=2,
    coord_elevation="top",
    coord_offset=-0.1,
    coord_font_size=8,
    coord_stroke=deepgray,
    coord_padding=2,
    fill=white,
    stroke=deepgray,
    stroke_width=1.2,
)

# Overlay (large hexes)
Hexagons(
    rows=4,
    cols=6,
    y=-2.49,  # 2.5 small hexes
    x=0,
    height=6.64,  # 4 x small hexes high
    margin_bottom=0.25,
    margin_left=2,
    hex_offset="odd",
    fill=None,
    stroke=darkgray,
    stroke_width=3,
)

# Tidy bottom edge
Rectangle(x=-0.2, y=-1.05, width=38.5, height=1.55, stroke=white, fill=white)

Save()
