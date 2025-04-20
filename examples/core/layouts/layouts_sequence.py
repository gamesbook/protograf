# -*- coding: utf-8 -*-
"""
Virtual layout examples for protograf

Written by: Derek Hohls
Created on: 19 May 2024
"""
from protograf import *

Create(filename="layouts_sequence.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5,
       font_size=8,
       stroke_width=0.5)

txt = Common(x=0, y=0, font_size=8, align="left")

# ---- sequence_values
Blueprint()
Text(common=txt, text="Sequence: text; values")
Sequence(
    text(text="{{sequence}}", x=1, y=5.5),
    setting=(10, 0, -2, 'number'),
    interval_x=0.5,
    )
Sequence(
    text(text="{{sequence}}", x=1, y=3.5),
    setting=('h','b',-2,'letter'),
    interval_y=0.5,
    interval_x=0.5,
    )
Sequence(
    text(text="{{sequence}}", x=1, y=3),
    setting=('B','H',2,'letter'),
    interval_y=-0.5,
    interval_x=0.5,
    )
Sequence(
    text(text="{{sequence}}", x=0.5, y=1),
    setting=(5, 11, 1, 'roman'),
    interval_x=0.5,
    )
Sequence(
    text(text="{{sequence}}", x=0.5, y=0.25),
    setting=(27, 57, 5, 'excel'),
    interval_x=0.5,
    )
PageBreak()

# ---- sequence_shapes
Blueprint()
Text(common=txt, text="Sequence: shapes, label")
Sequence(
    circle(cx=3.5, cy=5, radius=0.3, label="{{sequence}}"),
    setting=[4, 'B?', '', 'C!', 'VI'],
    interval_y=-0.7,
    )
Sequence(
    rectangle(x=0.25, y=0.25, height=0.75, width=1, label_size=8, label="${{sequence}}"),
    setting=(1, 3, 1, 'number'),
    interval_x=1.2,
    )
Sequence(
    [hexagon(x=0.5, y=1.5, radius=0.5, title_size=8, title="Fig. {{sequence}}"),
     circle(cx=1, cy=2, radius=0.2, fill="gray")],
    setting=('A', 'C', 1),
    interval_y=1.5,
    interval_x=0.5,
    )

#Save()
Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/layouts",
     names=[
        "sequence_values", "sequence_shapes",
     ]
)
