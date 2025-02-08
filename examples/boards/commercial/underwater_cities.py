"""
"Underwater Cities" board example for protograf

Written by: Derek Hohls
Created on: 27 October 2024
Notes:
    This is not a complete "copy" of the board; its just to show how
    some aspects could be implemented
"""
from protograf import *

Create(filename="underwater_cities.pdf", margin=0.0, paper=landscape(A2))

# Icons
money = rectangle(
    fill_stroke=gold, height=1.2, width=0.8, rounding=0.1,
    hatch_count=5, hatch='w', hatch_stroke=black,
    label_stroke=black, label_size=18)
pipe = image("images/pipe.png", width=2, height=0.75)
card_icon = rectangle(fill=white, label_stroke=black, label_size=32)
card_icon_small = rectangle(common=card_icon, height=1.2, width=0.8, rounding=0.1)
card_icon_med = rectangle(common=card_icon, height=1.7, width=1.2, rounding=0.15)
card_icon_large = rectangle(common=card_icon, height=2.2, width=1.6, rounding=0.2)

# Base Color - A2 page is 42cm x 59.4cm
deepsea = "#17366F"
Rectangle(x=0, y=0, width=59.4, height=42, fill=deepsea)

# World Map (#B6DCF4)
Image("images/world_map.png", x=7, y=6, width=52.4, height=32)

# Grid
Grid(x=0.25, y=0.4, side=1.25, stroke="#587CBC")

# Partial blur
Rectangle(x=0, y=0, width=59.4, height=42, fill=white, transparency=20)

# Outline
drect = Common(fill=None, stroke=grey, dashed=[0,0.05,0.05], rounding=0.5, stroke_width=2)

# Action Cards Slots: Red
rrect = rectangle(common=drect, x=-0.5, y=4.25, height=6., width=6.75)
Repeat(rrect, rows=5, cols=1, interval=7)

action_red = "#D4322D"
action_red_rect = rectangle(x=-0.5, y=4.5, width=6.5, height=5.5, fill_stroke=action_red, rounding=0.5)
Repeat(action_red_rect, rows=5, cols=1, interval=7)

action_red_dark = "#9D2622"
red_dark = Rectangle(y=4.5, x=0, width=2.5, height=5.5, fill_stroke=action_red_dark)
Repeat(red_dark, rows=5, cols=1, interval=7)

lock_red = image('images/padlock-open-red.png', x=1.5, y=7.25, width=1.5, height=1.5, rotation=270)
Repeat(lock_red, rows=5, cols=1, interval=3.5)

Rectangle(common=card_icon_med, x=4, y=34.5, label="A", rotation=270)

# Action Cards Slots: Orange
orect = rectangle(common=drect, y=36.75, x=6.75, width=6., height=6.75)
Repeat(orect, cols=5, rows=1, interval=7)

action_ong = "#FFAD01"
action_ong_rect = rectangle(x=7, y=37, width=5.5, height=6.5, fill_stroke=action_ong, rounding=0.5)
Repeat(action_ong_rect, cols=5, rows=1, interval=7)

action_ong_dark = "#FE9402"
ong_dark = Rectangle(y=40, x=7, width=5.5, height=2.5, fill_stroke=action_ong_dark)
Repeat(ong_dark, cols=5, rows=1, interval=7)

lock_ong = image('images/padlock-open-orange.png', x=10, y=41, width=1.5, height=1.5, rotation=180)
Repeat(lock_ong, rows=1, cols=5, interval=3.5)

Rectangle(common=card_icon_large, x=24, y=37.5, label="A", rotation=180)

# Action Cards Slots: Green
grect = rectangle(common=drect, y=-0.5, x=6.75, width=6., height=6.75)
Repeat(grect, cols=5, rows=1, interval=7)

action_grn = "#017A51"
action_grn_rect = rectangle(y=-0.5, x=7, width=5.5, height=6.5, fill_stroke=action_grn, rounding=0.5)
Repeat(action_grn_rect, cols=5, rows=1, interval_x=7)

action_grn_dark = "#005D33"
grn_dark = Rectangle(y=0, x=7, width=5.5, height=2.5, fill_stroke=action_grn_dark)
Repeat(grn_dark, cols=5, rows=1, interval_x=7)

lock_grn = image('images/padlock-open-green.png', x=9, y=0.5, width=1.5, height=1.5)
Repeat(lock_grn, rows=1, cols=5, interval_x=7)

Rectangle(common=card_icon_large, x=36, y=3, label="A")
Image(common=pipe, x=28.5, y=4)

# Special Cards
special_grn = "#4A8D86"
special_grn_design = Common(
    width=5.5, height=8.5, fill_stroke=special_grn, rounding=0.5,
    transparency=80, label="S", label_size=164, label_stroke="#69A8B9")
Repeat(
   rectangle(common=special_grn_design, y=9.5, x=34.5, ),
   cols=3, rows=2, interval_x=7, interval_y=9)
Rectangle(common=special_grn_design, y=13.5, x=27.5)

# Government Cards
gov_blue = "#666D8A"
gov_blue_rect = rectangle(y=24, x=11, width=5.5, height=8.5, fill_stroke=gov_blue, rounding=0.5, transparency=90)
Repeat(gov_blue_rect, cols=3, rows=1, interval=7)

# Free Action Space
free_action_top = "#016EB3"
free_action_btm = "#014B8A"
Rectangle(x=19.5, y=12, width=5.5, height=3.5, fill_stroke=free_action_top, rounding=0.5)
Rectangle(x=19.5, y=9.5, width=5.5, height=3, fill_stroke=free_action_btm, rounding=0.5)
Rectangle(common=drect, x=19, y=9, height=7, width=6.5)
# ... action icons
Rectangle(common=money, label="2", x=23.5, y=13.25)
Rectangle(common=card_icon_small, x=20, y=13.25)
Rectangle(common=card_icon_small, x=22.25, y=13.5)
Rectangle(common=card_icon_small, x=22.5, y=13)
EquilateralTriangle(x=21, y=13.5, side=0.7, rotation=60)

# Game Name
name_fill = "#4C588C"
name_stroke = "#788CCB"
name_rect = Common(fill=name_fill, stroke=name_stroke, stroke_width=2)
Rectangle(common=name_rect, x=44, y=1, width=10.5, height=4)
Rectangle(
    common=name_rect, x=44, y=3.75, width=10.5, height=1.25,
    label="PROJECT: UNDERWATER CITIES", label_size=18)

# Scoring Track
score_common = Common(
    cx=0, cy=0, radius=0.75, stroke_width=3, transparency=50,
    label_size=21, label_stroke=white)
score_base = circle(common=score_common, stroke="#11B6E4", fill="#008FCE")
score_5 = circle(
    common=score_common, stroke="#7BC9E6", fill="#3FA1BB", label="{{sequence}}")
score_10 = circle(
    common=score_common, stroke="#EEE544", fill="#B5CDB0", label="{{sequence}}")
score_track = RectangularLocations(
    x=7.5, y=7.75, cols=32, rows=19, interval=1.54,
    start="SE", direction="west", pattern="outer")
Layout(score_track,
       shapes=[score_base]*4 + [score_5] + [score_base]*4 + [score_10])

# Rightside Rect
Rectangle(x=57, y=4.5, width=5, height=33, fill_stroke="#D4D4DB", rounding=1.5)
Rectangle(
    x=57.4, y=6, width=2.4, height=30, fill_stroke="#554F52", rounding=0.4,
    hatch_count=12, hatch='w', hatch_stroke="#4E6B9A")
Sequence(
    text(x=58.5, y=6.8, font_size=24, stroke=grey, text="{{sequence}}"),
    setting=[1,2,3,4,' ',5,6,7,' ',8,9,10],
    interval_y=2.3)

# Player Order
play_order = "#D4D4DB"
Rectangle(x=9, y=9, width=6.5, height=12, fill_stroke=play_order, rounding=0.5)
Rectangle(
    x=11.6, y=11.5, width=3.7, height=8.5, fill="#2F4769",
    stroke=play_order, rounding=0.4,
    hatch_count=3, hatch='w', hatch_stroke=play_order)
Rectangle(
    x=9.2, y=11.5, width=2.4, height=8.5, fill="#2F4769",
    stroke=play_order, rounding=0.4,
    hatch_count=3, hatch='w', hatch_stroke=play_order)
Rectangle(
    x=9.2, y=9.2, width=6.1, height=2.4, fill="#2F4769",
    stroke=play_order, rounding=0.4)

Circle(cx=10.2, cy=10.8, radius=0.5, fill_stroke=steelblue)
Circle(cx=12.8, cy=10.8, radius=0.5, fill_stroke=orange)
Circle(cx=11.5, cy=9.9, radius=0.5, fill_stroke=dimgray)
Circle(cx=14, cy=9.9, radius=0.5, fill_stroke=darkorchid)

# Player VP
wreath = image('images/laurel-wreath.png', x=11.9, y=11.7, width=1.5, height=1.5)
Repeat(wreath, rows=4, cols=1, interval_y=2.1)
Sequence(
    text(x=10.4, y=18.4, font_size=32, stroke=orange, text="{{sequence}}."),
    setting=(1,4,1,'number'),
    interval_y=-2.1)
Sequence(
    text(x=12.8, y=18.4, font_size=32, stroke=white, text="{{sequence}}."),
    setting=(1,4,1,'number'),
    interval_y=-2.1)

Rectangle(common=money, label="1", x=13.75, y=14)

# Draw/Discards
disc_rect = Common(
    width=9.5, height=5.4,  rounding=0.5, transparency=80)
Rectangle(common=disc_rect, fill_stroke="#483D8B", x=44, y=36.5)
Rectangle(common=disc_rect, fill_stroke="#0275CC", x=44, y=29)
Image('images/trash-can-blue.png', x=49, y=39, width=2.5, height=2.5, rotation=90)



Save()
