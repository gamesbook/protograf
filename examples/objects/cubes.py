# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 3 August 2025
"""
from protograf import *

Create(
   filename="cubes.pdf",
    paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Cubes")

YELLOW = "#CEB316"  # old gold

Cube(x=0, y=0, height=1.5,
     fill=YELLOW)
Cube(x=0.75, y=1.5,
     height=1.5,
     shades=YELLOW)
Cube(x=1.5, y=3, height=1.5,
     shades=YELLOW,
     radii_stroke="white",
     radii_stroke_width=0.4)
Cube(x=2.5, y=4.5, height=1.5,
     shades=["#FFDC17", "#957F0A", "#CCB412"],
     radii_stroke="dimgray",
     radii_stroke_width=0.4)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'cubes',
    ]
)
