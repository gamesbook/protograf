"""
"Catan" board example for protograf

Written by: Derek Hohls
Created on: 30 March 2026
Notes:
"""
from protograf import *

Create(filename="catan.pdf", margin=0.5, paper="A4")

hxc = Common(height=3, stroke="silver", stroke_width=2,)
disc = Default(
    radius=0.66,
    label_stroke="black",
    stroke="silver", fill="#FFE19B",
    label_size="24",
    label_font="Times-Roman")
CX, CY = 10, 14

# The Hexagons
desert = hexagon(common=hxc, fill="#E6AD3A")
wheat = hexagon(common=hxc, fill="#FFCF1A")
pasture = hexagon(common=hxc, fill="#8CC53B")
hill = hexagon(common=hxc, fill="#F17B1D")
mountn = hexagon(common=hxc, fill="#C7B2A7")
forest = hexagon(common=hxc, fill="#0C4F16")

# The Discs
lb02 = circle(default=disc, label="2")
lb03 = circle(default=disc, label="3")
lb04 = circle(default=disc, label="4")
lb05 = circle(default=disc, label="5")
lb06 = circle(default=disc, label="6", label_stroke="red")
lb08 = circle(default=disc, label="8", label_stroke="red")
lb09 = circle(default=disc, label="9")
lb10 = circle(default=disc, label="10")
lb11 = circle(default=disc, label="11")
lb12 = circle(default=disc, label="12")

# "The Sea"
Hexagon(
    cx=CX, cy=CY, height=18,
    orientation="pointy",
    fill_stroke="#05B3EF")

# The Lands
HexHex(
    cx=CX, cy=CY, height=3, rings=2,
    shapes=[
        (0, [desert]),
        (1, [forest, hill, pasture, forest, wheat, mountn]),
        (2, [wheat, wheat, mountn, pasture, forest, hill,
             mountn, pasture, pasture, wheat, hill, forest]),
   ])

# The Numbers
HexHex(
    cx=CX, cy=CY, height=3, rings=2,
    shapes=[
        (1, [lb11, lb06, lb04, lb03, lb04, lb03]),
        (2, [lb09, lb12, lb10, lb02, lb09, lb10,
             lb08, lb05, lb11, lb06, lb05, lb08]),
    ])

Save()
