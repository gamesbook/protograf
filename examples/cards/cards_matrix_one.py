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
        # tomato, lime, aqua, gold, hotpink
        ['#FF6347', '#00FF00','#00FFFF', '#FFD700', '#FF69B4'],
        ['5', '3', '1'],
        # tapedrive, heart, snowflake
        ['\u2707', '\u2766', '\u2745']
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
    x=1, y=6.4,
    side=0.8,
    stroke=white)
value_top = text(
    x=1.8, y=6.8,
    font_size=28,
    text=T('{{VALUE}}'),
    align="centre",
    stroke=darkslategrey)
icon_btm = hexagon(
    x=3.8, y=0.9,
    side=0.8,
    stroke=white)
value_btm = text(
    x=4.6, y=1.9,
    font_size=28,
    align="centre",
    text=T('{{VALUE}}'),
    stroke=darkslategrey,
    rotation=180)
picture = text(
    x=3.0, y=3.3,
    stroke=white,
    font_size=76,
    text=T('{{IMAGE}}'))
deco_top = hexagon(
    x=1.1, y=6.5,
    side=0.7,
    fill=None,
    stroke=T('{{SUIT}}'))
deco_btm = hexagon(
    x=3.9, y=1.0,
    side=0.7,
    fill=None,
    stroke=T('{{SUIT}}'))

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
