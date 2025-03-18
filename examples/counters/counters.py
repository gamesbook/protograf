"""
`counters` script for protograf

Written by: Derek Hohls
Created on: 29 February 2016
Updated on: 22 September 2024
"""
from protograf import *

Create(filename='tannenberg.pdf')

# create counters
CounterSheet(
    counters=24, width=2.6, height=2.6, grid_marks=True, fill=yellow,
    spacing_x=2.6, spacing_y=1.3, grouping_cols=3, grouping_rows=2,)

# basic values
# http://cliparts.co/clipart/3214807
german_marker = 'images/ironcross_small.png'
# http://www.free-vectors.com/vector-russian-eagle/
russian_marker = 'images/russianeagle_small.png'
grey = "#B8BAB1"
brown = "#B6A378"

# basic shapes
german = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=grey)
russian = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=1, fill=brown)

out = rectangle(x=0.8, y=1.2, width=1.0, height=0.6, stroke_width=1.5, fill=None)
lu = line(x=0.8, y=1.2, x1=1.8, y1=1.8, stroke="black", stroke_width=1.5)
ld = line(x=0.8, y=1.8, x1=1.8, y1=1.2, stroke="black", stroke_width=1.5)
rect1 = rectangle(x=0.8, y=1.2, width=1.0, height=0.3, stroke_width=1.5, fill="black")
circ1 = circle(cx=1.3, cy=1.5, radius=0.1, stroke_width=0.1, fill="black")

# unit types
inf = group(out, lu, ld)
cav = group(out, lu)
HQ = group(out, rect1)
art = group(out, circ1)

# unit text
inf_A = text(font_name="Helvetica", font_size=18, x=1.3, y=0.5, text="2-3-4")
division = text(font_name="Helvetica", font_size=12, x=1.3, y=1.9, text="XX")
battalion = text(font_name="Helvetica", font_size=12, x=1.3, y=1.9, text="X")

# final counter designs
marker_german = group(
    german,
    image(german_marker, x=0.4, y=0.4, width=1.8, height=1.8))
marker_russian = group(
    russian,
    image(russian_marker, x=0.4, y=0.4, width=1.8, height=1.8))
inf_german = group(german, inf)
cav_german = group(german, cav)
inf_russian = group(russian, inf)
inf_russian_A = group(inf_russian, inf_A, division)
HQ_russian = group(russian, HQ)
art_russian = group(russian, art, battalion)

# generate counter images
Counter("1-5", inf_german)
Counter("6-9", cav_german)
Counter("10-12", HQ_russian)
Counter("13-15", inf_russian_A)
Counter("16-18", art_russian)
Counter("19-21", marker_german)
Counter("22-24", marker_russian)

Save()
