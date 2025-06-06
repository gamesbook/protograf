# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 19 August 2024
"""
from protograf import Blueprint, Create, Circle, Common, Text, Save, steps

Create(filename="clock.pdf",
       paper="A7",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=14, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="Basic Clock")

# basic clock frame
Circle(cx=3, cy=4.5, radius=2.5,
       stroke_width=6,
       label_size=6, label_my=1, label="PROTO")
# minutes
Circle(cx=3, cy=4.5, radius=2.3, radii=steps(0, 360, 6),
       stroke="white", fill=None, stroke_width=0.01,
       radii_length=0.15, radii_offset=2.2, radii_stroke_width=0.5, radii_stroke="black")
# hours
Circle(cx=3, cy=4.5, radius=2.3, radii=steps(0, 360, 30),
       stroke="white", fill=None, stroke_width=0.01,
       radii_length=0.3, radii_offset=2.2, radii_stroke_width=1.5, radii_stroke="black")
# centre
Circle(cx=3, cy=4.5, radius=.13, fill="black")
# hour hand
Circle(cx=3, cy=4.5, radius=1.8, radii=[330],
       stroke="white", fill=None,
       radii_length=2, radii_offset=-.5, radii_stroke_width=4, radii_stroke="black")
# minute hand
Circle(cx=3, cy=4.5, radius=1.8, radii=[210],
       stroke="white", fill=None,
       radii_length=2.3, radii_offset=-.5, radii_stroke_width=3, radii_stroke="black")

Save()
