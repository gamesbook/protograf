# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 28 June 2025
"""
from protograf import *

Create(filename="polyominoes.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

# ---- basic
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Basic")
Polyomino()
PageBreak()

# ---- simple
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Simple")
Polyomino(pattern=['110', '111'], fill="silver")
PageBreak()

# ---- invert
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Invert")
Polyomino(x=0, y=0, pattern=['110', '111'], fill="silver", invert="LR")
Polyomino(x=1, y=3, pattern=['110', '111'], fill="silver",  invert="TB")
PageBreak()

# ---- rotation
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Rotation")
Polyomino(x=0, y=0, pattern=['110', '111'], fill="silver", rotation=90)
Polyomino(x=2, y=3, pattern=['110', '111'], fill="silver", rotation=-90)
PageBreak()

# ---- color
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Colors")
Polyomino(
    x=0, y=1,
    pattern=['010', '234', '050'],
    stroke=None,
    fills=['red','yellow','silver','blue','green'],
    labels=[1,2,3,4,5])

Save(
    output='png',
    dpi=300,
    directory="../docs/source/examples/images/objects",
    names=[
        'polyomino_basic',
        'polyomino_simple',
        'polyomino_invert',
        'polyomino_rotation',
        'polyomino_color'
    ]
)
