# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 31 July 2025
"""
from protograf import *

Create(
   filename="dice_d6.pdf",
    paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

Blueprint(stroke_width=0.5)
Text(common=header, text="D6")

# ---- basic D6
D6(x=0, y=0)
D6(x=1, y=0, roll=2)
D6(x=0, y=1, roll=3)
D6(x=1, y=1, roll=4)
D6(x=0, y=2, roll=5)
D6(x=1, y=2, roll=6)

# ---- color rounded D6
red_yello = Common(
    pip_fill="gold", pip_stroke="orange",
    fill="red", rounding=0.175)
D6(x=2, y=0, common=red_yello)
D6(x=3, y=0, roll=2, common=red_yello)
D6(x=2, y=1, roll=3, common=red_yello)
D6(x=3, y=1, roll=4, common=red_yello)
D6(x=2, y=2, roll=5, common=red_yello)
D6(x=3, y=2, roll=6, common=red_yello)

# ---- color smaller D6
blu_wite = Common(
    pip_fill="white", pip_stroke="aqua",
    fill="blue", pip_fraction=0.15)
D6(x=0, y=3, common=blu_wite)
D6(x=1, y=3, roll=2, common=blu_wite)
D6(x=0, y=4, roll=3, common=blu_wite)
D6(x=1, y=4, roll=4, common=blu_wite)
D6(x=0, y=5, roll=5, common=blu_wite)
D6(x=1, y=5, roll=6, common=blu_wite)

# ---- sized, labelled & rotated D6
D6(x=2.6, y=3.6, side=0.8, roll=4, title="Title", heading="D6", label="4")
D6(cx=3.5, cy=5.5, side=0.5, roll=5, stroke_width=0.5, rotation=30)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'dice_d6',
    ]
)
