"""
Matrix cards script for protograf

Written by: Derek Hohls
Created on: 12 August 2024
"""
from protograf import *

# create deck
Create(filename='cards_matrix_one.pdf', margin_bottom=1.9)

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
Data(matrix=combos)  # (re)set no. of cards based on length

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
    stroke=T('{{SUIT}}'))

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
    stroke=T('{{SUIT}}'))

picture = text(
    x=3.1, y=5.5,
    stroke="white",
    font_size=76,
    align="centre",
    font_name='zapfdingbats',
    text=T('{{IMAGE}}'),
    )


# card setup
Card(
    "*",
    outline,
    picture,
    icon_top, icon_btm,
    deco_top, deco_btm,
    value_top, value_btm,
    )

Save()
