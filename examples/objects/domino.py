# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 16 December 2025
"""
from protograf import *

Create(
   filename="domino.pdf",
    paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")
red_yello = Common(
    pip_fill="gold", pip_stroke="orange",
    fill="red", rounding=0.175)
blu_wite = Common(
    pip_fill="white",
    pip_shape="diamond",
    pip_stroke="aqua",
    fill="blue", pip_fraction=0.15)

Blueprint(stroke_width=0.5)
Text(common=header, text="Domino")
# ---- basic Domino
Domino(x=0, y=0)
Domino(x=2, y=0, pips=(1, 2))
# ---- color rounded Domino
Domino(x=0, y=1, pips=(1, 3), common=red_yello)
Domino(x=2, y=1, pips=(1, 4), common=red_yello)
# ---- color smaller Domino
Domino(x=0, y=2, pips=(1, 5), common=blu_wite)
Domino(x=2, y=2, pips=(1, 6), common=blu_wite)

# ---- sized, labelled & rotated Domino
Domino(x=0.25, y=3.75, side=0.8, 
       pips=(2, 4), 
       title="Title", 
       heading="Domino", 
       label="2-4")
Domino(cx=3, cy=4, 
       side=0.5, 
       pips=(3, 5), 
       stroke_width=0.5, rotation=30)
Domino(cx=3, cy=5, 
       side=0.6, 
       centre_line=True,
       centre_line_stroke="red",
       centre_line_stroke_width=1,
       centre_line_length=0.22,
       centre_shape=dot(stroke="gold"),
       pips=(3, 5), 
       stroke_width=0.5, rotation=15)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'domino',
    ]
)
