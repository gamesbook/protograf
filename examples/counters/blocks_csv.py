"""
`blocks_csv` script for protograf

Written by: Derek Hohls
Created on: 9 August 2024
Updated on: 22 September 2024

Notes:

* Tile outline and dot colors:
    reds = "#790704"
    olives = "#937301"
    greens = "#57762C"
    blues = "#416E83"
* Images sourced from "images" subdirectory
"""
from protograf import *

# create counters
Create(filename='blocks_csv.pdf')

# load data; sets no. of counters based on rows in the CSV file
Data(filename="blocks.csv")

CounterSheet(width=2.9, height=2.9, grid_marks=True)

# common colors
blue = "#005F9C"
red = "#A71C20"
lbrown = "#F1D7B5"

# basic elements
tile_red = rectangle(x=0.0, y=0.0, width=2.9, height=2.9, stroke=red, fill=red)
tile_blue = rectangle(x=0.0, y=0.0, width=2.9, height=2.9, stroke=blue, fill=blue)
base = rectangle(x=0.2, y=0.2, width=2.5, height=2.5, stroke=brown, fill=lbrown)

# per-tile values and elements
title = text(
    font_name="Times-Roman", font_size=8, x=1.4, y=2, align="centre",
    text=T('{{TITLE}}'))
move = text(
    font_name="Times-Roman", font_size=12, x=0.6, y=0.5,
    text=T('{{MOVE}}'))
strength = text(
    font_name="Times-Roman", font_size=12, x=2.1, y=0.5,
    text=T('{{STRENGTH}}'))
outline = rectangle(
    x=0.45, y=0.45, width=2.0, height=2.0,
    stroke_width=1, stroke=T('{{BORDER}}'), fill=None)
pic = image(T('images/{{IMAGE}}'), x=0.7, y=0.8, width=1.5, height=1.1)

# "dots" templates
top4 = sequence(
     square(
         x=0.9, y=2.35, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}')),
     setting=(1, 4),
     interval_x=0.29)
right3 = sequence(
     square(
         x=2.3, y=1.0, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}')),
     setting=(1, 3),
     interval_y=0.29)
low2 = sequence(
     square(
         x=1.2, y=0.35, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}')),
     setting=(1, 2),
     interval_x=0.29)
left1 = square(
    x=0.35, y=1.3, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}'))
dots4 = group(top4, right3, low2, left1)

top3 = sequence(
     square(
         x=1.05, y=2.35, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}')),
     setting=(1, 3),
     interval_x=0.29)
right2 = sequence(
     square(
         x=2.3, y=1.2, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}')),
     setting=(1, 2),
     interval_y=0.29)
low1 = square(
    x=1.3, y=0.35, side=0.25, stroke=lbrown, stroke_width=1, fill=T('{{BORDER}}'))
dots3 = group(top3, right2, low1)

# shields
shield = Common(x=1.1, y=.8, height=0.9, width=0.7, hatch_count=1, hatch_width=3)
shield_blue = rectangle(
    common=shield, fill=blue, hatch_stroke=white, hatch='ne nw')
shield_red = rectangle(
    common=shield, fill=white, hatch_stroke=red, hatch='n e')

# counter assembly
Counter("all", S("{{ SIDE == 'English' }}", tile_red))
Counter("all", S("{{ SIDE == 'Scots' }}", tile_blue))
Counter("all", base, outline, move, title, strength, pic)
Counter("all", S("{{ DOTS == '4' }}", dots4))
Counter("all", S("{{ DOTS == '3' }}", dots3))
Counter("all", S("{{ SHIELD == 'red' }}", shield_red))
Counter("all", S("{{ SHIELD == 'blue' }}", shield_blue))

#Save(output='png')
Save()
