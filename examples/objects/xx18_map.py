# -*- coding: utf-8 -*-
"""
Example code for protograf XX18 command

Written by: Derek Hohls
Created on: 16 November 2026

Notes:
    * Map source is: https://simplemaps.com/svg/country/gh#all
"""
from protograf import *

Create(
    filename="xx18_map.pdf",
    paper="A4",
    margin=1.25,
    fill='skyblue')

Rectangle(
    x=-1.25, y=-1.25,
    height=22.5, width=21,
    fill_stroke="limegreen")
Rectangle(
    x=-1.25, y=19.5,
    height=6.2, width=4,
    fill_stroke="limegreen")

Image(
    "images/gh.svg",
    height=30, width=20,
    y=-1.7, x=-0.5)

map_pattern ="""
O O O O
 O O O .
. O O O
 O O O O
O O O O
 O O O O
O O O .
"""

xgh = XX18Game(
    rows=7,
    cols=4,
    fill=None,
    pattern=map_pattern)
XX18State(board=xgh)

Polyshape(
    fill_stroke="xred",
    points=[
      xgh.A7.se,
      xgh.A7.s,
      xgh.B8.sw,
      xgh.B8.s,
      xgh.D8.n,
      xgh.D8.ne,
      (21, xgh.D8.ne.y),
      (21, xgh.A7.se.y)
    ]
)
Polyshape(
    fill_stroke="xgray",
    points=[
      xgh.G7.n,
      xgh.G7.nw,
      xgh.G7.sw,
      xgh.G7.ne
    ]
)


def plot(**kwargs):
    for loc in kwargs['hexes']:
        Circle(cxy=loc.e, radius=0.5, fill="blue")
        Circle(cxy=loc.ssw, radius=0.5, fill="red")


xgf = XX18Game(
    rows=7,
    cols=4,
    label=True,
    fill=None,
    pattern=map_pattern,
    features=[
        ('B8', 'spike', 'w sw', 'medium',),
        ('G7', 'track', 'w,ne', ),
        ('C3', plot),
        ('D4', plot),
    ]
)
XX18State(board=xgf)

Text("Togo", xy=xgf.B8.c, stroke="white", font_size=18)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=['xx18_map']
)
