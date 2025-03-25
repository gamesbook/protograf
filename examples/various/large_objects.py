# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 9 August 2024
"""
from protograf import *

Create(filename="large_objects.pdf",
        paper="A8",
        margin_top=0.25,
        margin_left=0.75,
        margin_bottom=0.75,
        margin_right=0.2)

header = Common(x=0, y=6, font_size=12, align="left")

# ---- random chords
Blueprint(stroke_width=0.5)
Text(common=header, text="Random Chords")

for i in range(0, 200):
    Chord(shape=Circle(cx=2, cy=3, radius=2, fill=None),
          stroke_width=0.5,
          angle=Random(360), angle1=Random(360))
PageBreak()

# ---- Rondel
Blueprint(stroke_width=0.5)
Text(common=header, text="Rondel")

circ = Common(cx=2, cy=3, radius=2)
radii = list(range(0, 360, 60))
colrs = ["tomato", aqua, gold, "chartreuse", "lightsteelblue", white]
labels = ['Build', 'Trade', 'Income', 'Plant', 'Expand', 'Harvest']

# rondel colors
for colr, angle in zip(colrs, radii):
    Sector(
        common=circ,
        fill=colr, stroke="sienna", stroke_width=2,
        angle=420 - angle, angle_width=60)
# rondel text
Circle(
    common=circ,
    stroke="sienna", stroke_width=3,
    fill=None,
    radii=radii,
    radii_offset=0.75, radii_length=1,
    radii_stroke=None,
    radii_labels=labels,
    radii_labels_face="Times-Roman",
    dot=0.2)

PageBreak()

Save(
    output='png',
    dpi=300,
    directory="../docs/source/examples/images/various",
    names=[
        'chords', 'rondel'
    ]
)
