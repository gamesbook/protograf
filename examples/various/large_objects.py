# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 9 August 2024
"""
from protograf import *

Create(filename="large_objects.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

# ---- random chords
Blueprint(stroke_width=0.5)
Text(common=header, text="Random Chords")

for i in range(0, 200):
    Chord(shape=Circle(cx=2, cy=3, radius=2, stroke="black", fill=None),
          stroke_width=0.5,
          angle=Random(360), angle1=Random(360))
PageBreak()

# ---- Rondel
Blueprint(stroke_width=0.5)
Text(common=header, text="Rondel")

circ = Common(cx=2, cy=3, radius=2)
radii_angles = steps(0, 360, 60)
colrs = ["lightsteelblue", "cyan", "gold", "chartreuse", "tomato", "white", ]
labels = ['Build', 'Trade', 'Income', 'Plant', 'Explore', 'Harvest']

# rondel colors
for colr, angle in zip(colrs, radii_angles):
    Sector(
        common=circ,
        fill=colr,
        stroke="sienna", stroke_width=2,
        angle_start=angle - 30,
        angle_width=60)
# rondel text
Circle(
    common=circ,
    stroke="#A0522D",
    stroke_width=3,
    fill=None,
    radii=radii_angles,
    radii_offset=0.75,
    radii_length=1,
    radii_stroke=colrs,
    radii_stroke_width=0.01,
    radii_labels=labels,
    radii_labels_font="Times-Roman",
    dot=0.2)

PageBreak()

# ---- Compass Rose
# Blueprint(stroke_width=0.5,)
Text(common=header, text="Compass Rose")
Font("Times-Italic", size=14)
eye = Common(cx=2, cy=3)
Circle(
    common=eye,
    radius=2,
    stroke_width=1,
    fill=None,
    radii=steps(0, 360, 5),
    radii_offset=1.85,
    radii_length=0.1,
    radii_stroke_width=1,
    heading="N")
Circle(
    common=eye,
    radius=1.2,
    stroke_width=1,
    fill=None)
Star(
     common=eye,
     radius=1.4,
     rays=4,
     show_radii=True,
     rotation=45,
     stroke_width=1,
     slices=["black", "white"],
     radii_stroke_width=1,
     inner_fraction=0.25,
)
Star(common=eye,
     radius=2.2,
     rays=4,
     inner_fraction=0.25,
     stroke_width=1,
     slices=["black", "white"],
 )


Save(
    output='png',
    dpi=300,
    directory="../docs/source/examples/images/various",
    names=[
        'chords', 'rondel', 'compass_rose'
    ]
)
