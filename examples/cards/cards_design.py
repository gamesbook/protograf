"""
`cards_design` example for protograf

Written by: Derek Hohls
Created on: 19 February 2016
"""
from protograf import *

Create(filename='cards_design.pdf', margin_bottom=1.9)

# design deck
Deck(
    cards=18,
    height=8.8,
    width=6.3,
    rounding=0.3,
    fill=ivory)

# basic shapes
l1 = line(x=0.8, x1=5.6, y=7.1, y1=8.4, stroke=gold, stroke_width=2)
r1 = rectangle(x=0.7, y=7.0, width=5, height=1.5, stroke_width=1, rounding=0.2)
low = group(r1, l1)

# add shapes to cards
Card([1,2,3], low)
Card("4-6", r1)
Card("7,8,9", l1)

Card(steps(10,18,2), r1)
Card(steps(11,18,2), l1)

Save()
