"""
Play money as a Card Deck for protograf

Written by: Derek Hohls
Created on: 12 Februrary 2025
"""
from protograf import *

Create(filename='supreme.pdf', margin_bottom=2.5)

# deck data
cash = [
    ['VALUE', 'UNITS', 'COLOR', 'LINE', 'COPIES'],
    [1, "Million",  "#00FFFF","#000000", 10],
    [2, "Million", "#FFFFFF", "#000000",  10],
]
Data(data_list=cash)

# deck design
Deck(cards=20,
     height=5,
     width=9.5,
     fill=None,
     grid_marks=True,
     copy='COPIES')

# card elements
base = rectangle(x=0, y=0, width=9.5, height=5, line=None, fill=T('{{COLOR}}'))

edge = Common(x=0.35, length=8.8, stroke=T('{{LINE}}'), stroke_width=1)
btop = line(common=edge, y=0.3)
blow = line(common=edge, y=4.7)

stripe = line(y=1.3, x=0.35, length=8.8, stroke=T('{{LINE}}'), stroke_width=0.5)
stripes = repeat(stripe, rows=10, interval=2.4/9)

pl1 = polyline(points=[(2, 2.9), (4.2, 2.9), (4.75, 1.9), (5.3, 2.9), (7.5, 2.9)], stroke_width=3)
pl2 = polyline(points=[(2.2, 2.63), (4., 2.63), (4.55, 1.7), (4.35, 1.33)], stroke_width=3)
pl3 = polyline(points=[(2.4, 2.36), (3.8, 2.36), (4.25, 1.7), (4.05, 1.33)], stroke_width=3)
pl4 = polyline(points=[(7.3, 2.63), (5.5, 2.63), (4.95, 1.7), (5.15, 1.33)], stroke_width=3)
pl5 = polyline(points=[(7.1, 2.36), (5.7, 2.36), (5.25, 1.7), (5.45, 1.33)], stroke_width=3)
pl6 = polyline(points=[(4.4, 3), (4.75, 3.7), (4.95, 3.7), ], stroke_width=3)
pl7 = polyline(points=[(4.6, 2.8), (4.95, 3.5), (5.25, 3.5), ], stroke_width=3)
symbol = (pl1, pl2, pl3, pl4, pl5, pl6, pl7)

numbers = Common(text=T('{{VALUE}}'), font_name='Arial Bold', font_size=18)
num1 = text(common=numbers, align="left", x=0.3, y=0.4)
num2 = text(common=numbers, align="left", x=0.3, y=4.1)
num3 = text(common=numbers, align="right", x=9.2, y=0.4)
num4 = text(common=numbers, align="right", x=9.2, y=4.1)
values = group(num1, num2, num3, num4)

header = text(text=T('{{UNITS}}'), font_name='Arial Bold', font_size=18, x=4.75, y=4.1)
footer = text(text=T('{{UNITS}}'), font_name='Arial Bold', font_size=18, x=4.75, y=.4)

parts = group(
    base, btop, blow, header, footer, stripes, values, symbol)

# card setup
Card("*", parts)

Save()
