"""
Matrix cards script, with "joker" cards, for protograf

Written by: Derek Hohls
Created on: 12 August 2024
"""
from protograf import *

# create deck
Create(filename='cards_matrix_two.pdf', margin=1, margin_bottom=1.9)

# generate data for cards
# Note: symbols are from https://www.w3schools.com/charsets/ref_utf_dingbats.asp
combos = Matrix(
    labels=['SUIT', 'VALUE', 'IMAGE'],
    data=[
        # "tomato", "chartreuse", aqua, gold, hotpink
        ['#FF6347', '#00FF00','#00FFFF', '#FFD700', '#FF69B4'],
        ['5', '3', '1'],
        # plane, star, snowflake
        ['\x28', 'H', '\x64']
    ])
Data(matrix=combos, extra=9)  # (re)set no. of cards based on length

# deck design
Deck(cards=27,
     height=8.8,
     width=6.3,
     rounding=0.5,
     grid_marks=True)

# card layout elements
outline = rectangle(
    x=0.6, y=0.5,
    height=7.8, width=5.1,
    rounded=0.5,
    fill_stroke=T('{{SUIT}}')
    )

icon_top = hexagon(
    x=1, y=0.9,
    side=0.8,
    stroke="white")
value_top = text(
    x=1.8, y=1.9,
    font_size=28,
    text=T('{{VALUE}}'),
    align="centre",
    stroke="darkslategray")
deco_top = hexagon(
    x=1.1, y=1,
    side=0.7,
    fill=None,
    stroke_width=1,
    stroke="gray")

icon_btm = hexagon(
    x=3.8, y=6.6,
    side=0.8,
    stroke="white")
value_btm = text(
    x=4.7, y=7,
    font_size=28,
    align="centre",
    text=T('{{VALUE}}'),
    stroke="darkslategray",
    rotation=180)
deco_btm = hexagon(
    x=3.9, y=6.7,
    side=0.7,
    fill=None,
    stroke_width=1,
    stroke="gray")

picture = text(
    x=3.1, y=5.5,
    stroke="white",
    font_size=76,
    align="centre",
    font_name='zapfdingbats',
    text=T('{{IMAGE}}'),
    )


# card setup
Card("1-45",
     outline,
     picture,
     icon_top, icon_btm,
     deco_top, deco_btm,
     value_top, value_btm,
)

# custom cards
rectC = rectangle(
    y=0.5,
    height=7.8,
    width=1.02,
    rounding=0.2,
    stroke="white")
Card("46-48",
     rectangle(common=rectC, x=0.6, fill='#FF0000'),
     rectangle(common=rectC, x=1.62, fill='#FFD700'),
     rectangle(common=rectC, x=2.64, fill='#9ACD32'),
     rectangle(common=rectC, x=3.66, fill='#00BFFF'),
     rectangle(common=rectC, x=4.68, fill='#FF69B4')
)

hexN = Common(
    side=1.5,
    fill=None,
    font_size=28,
    stroke="black",
    stroke_width=2)
hex_in = hexagon(
    side=1.0,
    fill=None,
    stroke="black",
    stroke_width=.5)
Card("49-51",
     hexagon(common=hexN, cx=2.0, cy=1.8, centre_shape=hex_in, label="1"),
     hexagon(common=hexN, cx=3.3, cy=4.4, centre_shape=hex_in, label="3"),
     hexagon(common=hexN, cx=4.6, cy=7.0, centre_shape=hex_in, label="5"),
)

# circle + icons ['\x28', 'H', '\x64']
circle_icon = Common(fill="black", stroke="white", radius=1.25, font_size=48)
Card("52-54",
     circle(common=circle_icon, cx=1.8, cy=1.8, label='\x28', label_font='zapfdingbats'),
     circle(common=circle_icon, cx=3.1, cy=4.4, label='H', label_font='zapfdingbats'),
     circle(common=circle_icon, cx=4.4, cy=7.0, label='\x64', label_font='zapfdingbats'),
)

Save()
