"""
Customised Hexagons grid for an SPI-style map

Written by: Derek Hohls
Created on: 1 May 2026

Notes:
    * Based off of the map for the SPI game
      "Tannenberg and the Opening Battles in the East 1914"
"""
from protograf import *

# colors
TOWN = "#3E91DB"
RIVER = "#9AC4D5"
HEX = "#EBE2B4"
FORT = "#E38A01"
RAIL = "black"

Create(
    filename="tannenburg_spi.pdf",
    paper="A5-l",
    margin=0.75,
    margin_left=2,
    stroke_width=0.5,
    stroke="grey",
    fill="grey",
)

hg = Hexagons(
    height=1.58,  # 5/8"
    x=0, y=0,
    fill="#EBE2B4",
    rows=8, cols=12)

# forests
Image("images/forest_large.png", height=4.5, width=4.5,
      cx=hg.cell("0505").geo.c.x - 0.4, cy=hg.cell("0505").geo.c.y + 0.5)

# lakes

# broken

# River
GridLine(
    hg,
    start="0108",
    vertex="se",
    # edges="ne, nw, ne, nw, ",
    edges="ne,nw,"*3+"ne,e,"+"ne,nw,"*3+"ne,"+"e,se,"*3+\
          "e,ne,e,se,e,ne,e,ne,"+"e,se,"*2+"e",
    stroke=RIVER,
    stroke_width=6,
    stroke_ends="rounded")

# Russian Fortress
forts = Common(height=1.3, stroke=FORT, stroke_width=6, fill=None)
Hexagon(cxy=hg.cell("0303").geo.c, common=forts)
Hexagon(cxy=hg.cell("0802").geo.c, common=forts)

# Labels
reinf = Common(font_size=21, stroke=FORT)
Text("A", xy=hg.cell("0104").geo.c, common=reinf)
Text("B", xy=hg.cell("0701").geo.c, common=reinf)
Text("C", xy=hg.cell("1101").geo.c, common=reinf)

# Towns
Dot(x=hg.cell("1108").geo.c.x+0.2, y=hg.cell("1108").geo.c.y+0.2,
    stroke=TOWN, title="Suvalki", title_size=8)
Dot(x=hg.cell("0802").geo.c.x+0.2, y=hg.cell("0802").geo.c.y-0.4,
    stroke=TOWN, title="Olita", title_size=8)

# Border


# Single Rails
GridLine(
    hg,
    start="0701",
    perbis="n",
    paths="s,s,s,se,s,se,s",
    stroke=RAIL,
    stroke_width=1,
    dashed=[0.3, 0.1])


# Double Rails
GridLine(
    hg,
    start="0508",
    perbis="s",
    paths="n,nw,n,n,nw,n,n,n,n",
    stroke=RAIL,
    stroke_width=1)
GridLine(
    hg,
    start="1101",
    perbis="n",
    paths="s,se,se",
    stroke=RAIL,
    stroke_width=1)


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

# bLOCKed
GridLine(hg,start="0904",vertex="sw", edges="nw,ne", stroke="black",stroke_width=4)
GridLine(hg,start=["1005", "1104"],vertex="sw",edges="e", stroke="black",stroke_width=4)
# GridLine(hg,start=["0709", "1107"],vertex="se",edges="ne", stroke="black",stroke_width=4)


Save(
    output='png',
    dpi=300,
    directory="/tmp/demo",
)
