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
Text(common=txt, text="Sequence: Values #1")
Sequence(
    text(text="{{sequence}}", x=1, y=3),
    setting=(10, 0, -2, 'number'),
    interval_x=0.5,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Values #2")
Sequence(
    text(text="{{sequence}}", x=1, y=2.5),
    setting=('h', 'b', -2, 'letter'),
    interval_y=0.5,
    interval_x=0.5,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Values #3")
Sequence(
    text(text="{{sequence}}", x=1, y=4),
    setting=('B', 'J', 2, 'letter'),
    interval_y=-0.5,
    interval_x=0.5,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Values #4")
Sequence(
    text(text="{{sequence}}", x=0.5, y=3),
    setting=(5, 11, 1, 'roman'),
    interval_x=0.5,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Values #5")
Sequence(
    text(text="{{sequence}}", x=0.5, y=3),
    setting=(27, 57, 5, 'excel'),
    interval_x=0.5,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Values #6")
Sequence(
    text(text="{{sequence}}", x=2, y=1),
    setting=(27, 57, 5, 'excel'),
    interval_y=[.5, .75, .65, .55, 1.25, .85, 1.05]
    )
PageBreak()

# ---- sequence_shapes
Blueprint()
Text(common=txt, text="Sequence: Shapes #3")
Sequence(
    circle(cx=2, cy=4, radius=0.3, label="{{sequence}}"),
    setting=[4, 'B?', '', 'C!', 'VI'],
    interval_y=-0.7,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Shapes #1")
Sequence(
    rectangle(x=0.25, y=0.25, height=1, width=1,
              label_size=8, label="${{sequence}}"),
    setting=(1, 3, 1, 'number'),
    interval_x=1.2,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Shapes #2")
Sequence(
    [hexagon(cx=1, cy=1, radius=0.5, title_size=8, title="Fig. {{sequence}}"),
     circle(cx=1, cy=1, radius=0.2, fill="gray")],
    setting=('A', 'C', 1),
    interval_y=2,
    interval_x=1,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Shapes #4")
Sequence(
    [square(x=1.5, y=1, side=0.75, rounded=True, label_size=10, label ="{{sequence}}")],
    setting=list('DIANA'),
    interval_y=0.8,
    interval_x=0.0,
    )
PageBreak()

Blueprint()
Text(common=txt, text="Sequence: Shapes #5")
Sequence(
    [polygon(
        cx=2, cy=0.5,
        sides=7, radius=0.5,
        # fill="{{sequence}}",
        label_size=7, label="{{sequence}}")],
    setting=["red", "orange", "yellow", "green", "blue"],
    interval_y=[1.25, 1.5, 1, 1.25, 0.75],
    interval_x=[-0.5, 0.0, 0.4, 1.0, 2.0],
    )

Save(
     output='png',
     dpi=300,
     directory="../docs/source/images/layouts",
     names=[
        "sequence_values1",
        "sequence_values2",
        "sequence_values3",
        "sequence_values4",
        "sequence_values5",
        "sequence_values6",
        "sequence_shape1",
        "sequence_shape2",
        "sequence_shape3",
        "sequence_shape4",
        "sequence_shape5",
     ]
)
