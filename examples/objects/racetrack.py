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

PageBreak()


Blueprint(stroke_width=0.5)
Text(common=txt, text="RaceTrack: Joined Paths")

joined = Common(
    height=0.5,
    fill="silver",
    stroke_width=0.5,
    lanes=3,
    no_ends=True)

rectJ = rectangle(
    common=joined,
     x=1.5)
bandJ = band(
    common=joined,
    cx=2, cy=4.5, radius=1,
    angle_width=180)

RaceTrack(stages=[rectJ, bandJ, rectJ, bandJ])

RaceTrack(stages=[bandJ, bandJ])

PageBreak()


Blueprint(stroke_width=0.5)
Text(common=txt, text="RaceTrack: Complex Path")

mixed = Common(
    height=0.5,
    stroke_width=0.5,
    lanes_stroke_width=0.5,
    sections_stroke_width=0.25,
    sections_stroke="red",
    lanes=2)

r1 = rectangle(
    common=mixed,
    x=1.25,
    width=1.1,
    sections=[0.25, 0.9])
r2 = rectangle(
    common=mixed,
    width=1,
    lanes=[0.25, 0.75], sections=2)
r3 = rectangle(
    common=mixed,
    width=1.75,
    sections=[
        [0.333, 0.66],
        [1/4, 1/2, 3/4], [1/3, 2/3]])

b1 = band(
    common=mixed,
    radius=1,
    angle_width=90,
    sections=3)
b2 = band(
    common=mixed,
    radius=1,
    angle_width=120,
    sections=[[0.5], [0.25, 0.9]])
b3 = band(
    common=mixed,
    radius=1.95,
    angle_width=30,
    sections=[[0.5], [0.33, 0.66]])

RaceTrack(stages=[r1, b1, r2, b2, r3, b2, b3])

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'racetrack_simple',
        'racetrack_joined',
        'racetrack_complex',
    ]
)
