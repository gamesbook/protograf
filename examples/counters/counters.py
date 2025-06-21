"""
`counters` script for protograf

Written by: Derek Hohls
Created on: 29 February 2016
Updated on: 8 April 2025
"""
from protograf import *

Create(filename='tannenberg.pdf', margin_left=1.5, margin_top=1.5)

# create counters
CounterSheet(
    counters=24, width=2.6, height=2.6,
    grid_marks=True,
    spacing_x=2.6, spacing_y=1.3,
    grouping_cols=3, grouping_rows=2)

# markers
# Source: http://cliparts.co/clipart/3214807
german_marker = image('images/ironcross_small.png', x=0.4, y=0.4, width=1.8, height=1.8)
# Source: http://www.free-vectors.com/vector-russian-eagle/
russian_marker = image('images/russianeagle_small.png', x=0.4, y=0.4, width=1.8, height=1.8)

# national colors
german = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=0.5, fill="gray")
russian = rectangle(x=0, y=0, width=2.6, height=2.6, stroke_width=0.5, fill="peru")

# basic shapes
out = rectangle(x=0.8, y=1, width=1.2, height=0.8, stroke="black", stroke_width=1.5, fill=None)
lu = line(x=0.8, y=1, x1=2, y1=1.8, stroke="black", stroke_width=1.5)
ld = line(x=0.8, y=1.8, x1=2, y1=1, stroke="black", stroke_width=1.5)
rect1 = rectangle(x=0.8, y=1.4, width=1.2, height=0.4, stroke="black", stroke_width=1.5, fill="black")
circ1 = circle(cx=1.4, cy=1.4, radius=0.15, stroke="black", stroke_width=1, fill="black")

# unit text
ratings = Common(font_name="Helvetica", font_size=18, x=1.4, y=2.4)
rating_A = text(common=ratings, text="2-3-4")
rating_B = text(common=ratings, text="1-2-4")
rating_H = text(common=ratings, text="2-1-8")
rating_R = text(common=ratings, text="4-1-2")
rating_Q = text(common=ratings, text="0-0-4")

classify = Common(font_name="Helvetica", font_size=12, x=1.4, y=0.8)
division = text(common=classify, text="XX")
battalion = text(common=classify, text="X")

# unit designations
inf = group(out, lu, ld)
cav = group(out, lu)
HQ = group(out, rect1)
art = group(out, circ1)

# national units: german
art_german = group(german, art, rating_R)
inf_german = group(german, inf, division, rating_A)
cav_german = group(german, cav, battalion, rating_H)
HQ_german = group(german, HQ, rating_Q)
# national units: russian
inf_russian = group(russian, inf, division, rating_B)
HQ_russian = group(russian, HQ, rating_Q)
art_russian = group(russian, art, rating_R)

# counter assignments
Counter("1-4", inf_german)
Counter("5", art_german)
Counter("6-9", cav_german)
Counter("10-12", HQ_russian)
Counter("13-15", inf_russian)
Counter("16-18", art_russian)
Counter("19-20", HQ_german)
Counter("21-22", german, german_marker)
Counter("23-24", russian, russian_marker)

Save()
