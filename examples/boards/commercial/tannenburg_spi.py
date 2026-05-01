"""
Customised Hexagons grid for SPI-type map

Written by: Derek Hohls
Created on: 1 May 2026
"""
from protograf import *

Create(
    filename="tannenburg_spi.pdf",
    paper="A5-l",
    margin=0.75,
    margin_left=2,
    stroke_width=0.5,
    stroke="grey",
)

hg = Hexagons(
    height=1.58,  # 5/8"
    x=0, y=0,
    fill="#EBE2B4",
    rows=8, cols=12)

# forests
Image("images/forest_large.png", x=3.8, y=5.5, height=4.5, width=4.5)

# lakes

# broken


# Russian Fortress


# Towns


# River
GridLine(
    hg,
    start="0108",
    vertex="se",
    edges="ne,nw,ne,nw",
    stroke="#9AC4D5",
    stroke_width=6,
    stroke_ends="rounded")

# Border


# Single Rails


# Double Rails


# final grid
Hexagons(
    height=1.58,  # 5/8"
    x=0, y=0,
    rows=8, cols=12,
    stroke="grey",
    fill=None,
    coord_elevation='top',
    coord_stroke="grey"
)

Save(
    output='png',
    dpi=300,
    directory="/tmp/demo",
)
