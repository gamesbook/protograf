# -*- coding: utf-8 -*-
"""
Repeat layout examples for protograf

Written by: Derek Hohls
Created on: 19 December 2024
"""
from protograf import *

Create(filename="layouts_repeat.pdf",
       paper="A8",
       margin=0.75,
       margin_right=0.2, margin_top=0.2,
       font_size=10,
       stroke_width=0.5)

header = Common(x=0, y=6, font_size=7, align="left")
marble = circle(cx=1, cy=1, radius=0.25, fill="chartreuse")

Blueprint(stroke_width=0.5)
Text(common=header, text="Repeat: cols&rows: interval=0")
Repeat(marble, cols=4, rows=5)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Repeat: cols&rows: interval=1")
Repeat(marble, cols=4, rows=5, interval=1)
PageBreak()

Blueprint(stroke_width=0.5, subdivisions=4)
Text(common=header, text="Repeat: interval: across < down")
Repeat(marble, cols=4, rows=4, interval_x=0.75, interval_y=1.25)
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Repeat: across (cols 2 & 4 only)")
Repeat(marble, cols=4, rows=5, interval=1, across=(2, 4))
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Repeat: down (rows 1, 3 & 5 only)")
Repeat(marble, cols=4, rows=5, interval=1, down=(1, 3, 5))
PageBreak()

Blueprint(stroke_width=0.5)
Text(common=header, text="Repeat: across&down")
Repeat(marble, cols=4, rows=5, interval=1, across=(2, 4), down=(1, 3, 5))
PageBreak()

# Save()
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/layouts",
     names=[
        "repeat_basic",
        "repeat_interval", "repeat_interval_acrossdown",
        "repeat_across", "repeat_down", "repeat_acrossdown",

     ]
)
