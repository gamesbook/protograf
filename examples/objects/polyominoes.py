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
Polyomino()  # a "monomo"
PageBreak()

# ---- pattern
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Pattern")
Polyomino(pattern=['100', '111'], fill="silver")
PageBreak()

# ---- gap
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Gap (0.1)")
Polyomino(x=0, fill="silver", pattern=['100', '111'], side=1.2, gap=0.1, rounding=0.1)
PageBreak()

# ---- invert
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Invert")
Polyomino(x=0, y=0, pattern=['100', '111'], fill="silver", invert="LR")
Polyomino(x=1, y=3, pattern=['100', '111'], fill="grey", invert="TB")
PageBreak()

# ---- flip
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Flip")
Polyomino(x=0, y=0, pattern=['100', '111'], fill="silver", flip="north")
Polyomino(x=2, y=3, pattern=['100', '111'], fill="grey", flip="south")
PageBreak()

# ---- outline
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Outline")
Polyomino(
    pattern=['100', '111'],
    fill_stroke="silver",
    outline_stroke='red', outline_width=2)
PageBreak()

# ---- props
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Props")
Polyomino(
    x=0, y=1,
    pattern=['010', '234', '050'],
    stroke=None,
    fills=['red', 'yellow', 'silver', 'blue', 'green'],
    strokes=['yellow', 'silver', 'blue', 'green', 'red'],
    stroke_width=2,
    label_stroke="black",
    label_size=8,
    labels=['red', 'yellow', 'silver', 'blue', 'green'],
)
PageBreak()

# ---- shapes
Blueprint(stroke_width=0.5)
Text(common=header, text="Polyomino: Shapes")
Polyomino(
    x=0, y=1,
    pattern=['010', '232'],
    # stroke="black",
    fill="silver",
    centre_shapes=[
        circle(radius=0.3),
        dot(),
        hexagon(radius=0.3)]
)
PageBreak()

# ---- generic pattern
Blueprint(stroke_width=0.5)
Text(common=header, text="AdHoc Design")
Polyomino(
    x=0, y=1,
    pattern=['1001', '0110', '0100', '1001'],
    fill="silver")

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'polyomino_basic',
        'polyomino_pattern',
        'polyomino_gap',
        'polyomino_invert',
        'polyomino_flip',
        'polyomino_outline',
        'polyomino_color',
        'polyomino_shapes',
        'polyomino_generic',
    ]
)
