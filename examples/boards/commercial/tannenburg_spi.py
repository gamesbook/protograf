"""
Customised Hexagons grid for an SPI-style map

Written by: Derek Hohls
Created on: 1 May 2026

Notes:
    * Based off of the map for the SPI game
      "Tannnberg and the Opening Battles in the East 1914"
    * Images created manually by "eye-balling" the orginal map
"""
from protograf import *

# colors
TOWN = "#0E6EC3"
RIVER = "#9AC4D5"
HEX = "#EBE2B4"
FORT = "#E38A01"
RAIL = "black"
HEXES = "#EBE2B4"  # background

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
    fill=HEXES,
    rows=8, cols=12)

imsize = Common(height=1.58, width=1.58)

# Swamps
Image("images/marsh.png", common=imsize, cxy=hg.cxy("0106"))
Image("images/marsh.png", common=imsize, cxy=hg.cxy("0107"))

# Broken
Image("images/broken.png", common=imsize, cxy=hg.cxy("1104"), rotation=60)
Image("images/broken.png", common=imsize, cxy=hg.cxy("1106"), rotation=90)
Image("images/broken.png", common=imsize,
      cx=hg.cxy("1004").x, cy=hg.cxy("1004").y+0.6, rotation=90)
Image("images/broken.png", common=imsize, cxy=hg.cxy("1005"), rotation=270)
Image("images/broken.png", common=imsize,
      cx=hg.cxy("1107").x, cy=hg.cxy("1107").y-0.7, rotation=70)

# Lakes
Image("images/lake.png", common=imsize,
      cx=hg.cxy("1005").x, cy=hg.cxy("1005").y+0.8)
Image("images/lake.png", height=1.20, width=1.3,
      cx=hg.cxy("1104").x, cy=hg.cxy("1104").y+0.8)
Image("images/lake.png", common=imsize,
      cx=hg.cxy("1107").x+0.6, cy=hg.cxy("1107").y+0.5, rotation=150)

# River
GridLine(
    hg,
    start="0108",
    point="se",
    edges="ne,nw,"*3+"ne,e,"+"ne,nw,"*3+"ne,"+"e,se,"*3+\
          "e,ne,e,se,e,ne,e,ne,"+"e,se,"*2+"e",
    stroke=RIVER,
    stroke_width=6,
    stroke_ends="rounded",
    wave_style="wave",
    wave_height=0.2)

# Forests
Image("images/forest_large.png", height=4.5, width=4.5,
      cx=hg.cxy("0505").x-0.4, cy=hg.cxy("0505").y+0.5)
Image("images/forest_small.png", common=imsize, cxy=hg.cxy("0108"), rotation=90)
Image("images/forest_small.png", common=imsize, cxy=hg.cxy("0208"))
Image("images/forest_small.png", common=imsize, cxy=hg.cxy("1202"))

# Russian Fortress
forts = Common(height=1.3, stroke=FORT, stroke_width=6, fill=None)
Hexagon(cxy=hg.cxy("0303"), common=forts)
Hexagon(cxy=hg.cxy("0802"), common=forts)

# Towns
Dot(x=hg.cxy("1108").x+0.2, y=hg.cxy("1108").y+0.1,
    stroke=TOWN, title="Suvalki", title_size=8)
Dot(x=hg.cxy("0802").x+0.2, y=hg.cxy("0802").y-0.4,
    stroke=TOWN, title="Olita", title_size=8)
Dot(x=hg.cxy("0302").x+0.4, y=hg.cxy("0302").y-0.3,
    stroke=TOWN, label="Kovno", label_size=8, label_mx=0.8)

# Border
GridLine(
    hg,
    start="0108",
    point="nw",
    edges="e,se,e,ne,e,se,e,se",
    stroke="grey",
    stroke_width=3,
    dashed=[0.3, 0.1, 0.1, 0.1]
)

# Single-track Rails
sngrl = Common(stroke=RAIL,stroke_width=1, dashed=[0.3, 0.1])
GridLine(
    hg,
    start="0701",
    point="n",
    paths="s,s,s,se,s,se,s,c",
    common=sngrl)
GridLine(
    hg,
    start="1207",
    point="se",
    paths="sw,nw,nw,nw,sw,nw,nw,n,nw,nw",
    common=sngrl)
GridLine(
    hg,
    start="0903",
    point="nw",
    paths="s,"*4,
    common=sngrl)
GridLine(
    hg,
    start="1102",
    point="c",
    paths="sw,s,sw,c",
    common=sngrl)

# Double-track Rails
dbrl = Common(stroke=RAIL,stroke_width=1)
GridLine(
    hg,
    start="0508",
    point="s",
    paths="n,nw,n,n,nw,n,n,n,n",
    common=dbrl)
GridLine(
    hg,
    start="1101",
    point="n",
    paths="s,se,se",
    common=dbrl)
GridLine(
    hg,
    start="0104",
    point="sw",
    paths="ne,ne,c",
    common=dbrl)

# Labels
reinf = Common(font_size=21, stroke=FORT)
Text("A", xy=hg.cxy("0104"), common=reinf)
Text("B", xy=hg.cxy("0701"), common=reinf)
Text("C", xy=hg.cxy("1101"), common=reinf)

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

# Blocked
GridLine(hg, start="0904", point="sw", edges="nw,ne", stroke="black", stroke_width=4)
GridLine(hg, start=["1005","1104"], point="sw", edges="e", stroke="black", stroke_width=4)
GridLine(hg,start="1107",point="se",edges="ne", stroke="black",stroke_width=4)

Save(
    output='png',
    dpi=300,
    directory="/tmp/demo",
)
