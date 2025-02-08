# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 9 August 2024
"""
from protograf import *

Create(filename="chords.pdf",
        paper=A8,
        margin_top=0.5,
        margin_left=0.15,
        margin_bottom=0.15,
        margin_right=0.2)

header = Common(x=0, y=6, font_size=8, align="left")
Blueprint(stroke_width=0.5)
Text(common=header, text="Random Chords")

for i in range(0, 200):
    Chord(shape=Circle(cx=2, cy=2, radius=2, fill=None),
          angle=Random(360), angle1=Random(360))

Save()
