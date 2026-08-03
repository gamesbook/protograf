# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 3 August 2026
"""
from protograf import *

Create(
   filename="racetrack.pdf",
    paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

txt = Common(x=0, y=0, font_size=8, align="left")

Blueprint(stroke_width=0.5)
Text(common=txt, text="RaceTrack: Simple Paths")

# ---- rectangles
basics = Common(
    width=1.0,
    stroke="black")

rect1 = rectangle(common=basics, fill="gold", height=0.5, x=2)
rect2 = rectangle(common=basics, fill="aqua", height=1.0)

RaceTrack(stages=[rect1, rect2])

# ---- bands
styles = Common(
    stroke="black",
    radius=1,
    angle_width=60)

band1 = band(common=styles, fill="gold", height=0.5, cx=2, cy=4, angle_start=30)
band2 = band(common=styles, fill="aqua", height=0.25)

RaceTrack(stages=[band1, band2])


Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'racetrack_simple',
    ]
)
