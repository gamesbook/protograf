# -*- coding: utf-8 -*-
"""
Logo for protograf

Written by: Derek Hohls
Created on: 5 January 2025

Notes:
    Not sure what font to use for your logo ... watch
    https://www.youtube.com/watch?v=j7SByXWWVzU
"""
from protograf import *

Create(filename="logo.pdf",
        paper=landscape(A8),
        margin_top=0.1,
        margin_left=0.6,
        margin_bottom=0.6,
        margin_right=0.1)

header = Common(x=0, y=6, font_size=8, align="left")

#Blueprint(stroke_width=0.5, subdivisions=5)
#Text(common=header, text="Logo")

sanserif = Font("Courier", size=24, stroke="#3085AC")
Text(x=0, y=2, text='proto', width=3, height=2,
     wrap=True, align="left", stroke="#3085AC")
sans = Font("Helvetica", size=20, stroke="#3085AC")
Text(x=2.58, y=1.85, text='<b>graf</b>', width=2, height=2,
     wrap=True, align="left", stroke="#3085AC")

Hexagon(
    cx=1.27, cy=1.33,
    stroke="#3085AC",
    stroke_width=1.1,
    dot=0.03,
    radius=0.2,
)
Polygon(
    cx=2.29, cy=1.33,
    stroke="#3085AC",
    stroke_width=1.1,
    radius=0.2,
    radii='*',
    radii_stroke_width=0.5,
    sides=8
)

Save(
    output='png',
    directory="docs/source/examples/images/various"
)
