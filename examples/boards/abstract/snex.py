# -*- coding: utf-8 -*-
"""
A dynamic boardgame example for protograf

Written by: Derek Hohls
Created on: 27 September 2025

Sources:
   * Snex game: https://boardgamegeek.com/thread/3581837/new-game-snex
   * Stone images: https://github.com/zpmorgan/gostones-render
"""
from protograf import *
# setup
TAN = "#ECC185"
LINE = "#BB9564"
STAR = "yellow"
Create(filename="snex.pdf",
       paper_width=8.5, paper_height=8.5,
       margin=0.25,
       fill=TAN, stroke_width=1)
# board & pieces
rect = RectangularLocations(x=0.45, y=0.45, cols=8, rows=8, interval=1)
wht = image("go_white.png", height=0.9, width=0.9)
blk = image("go_black.png", height=0.9, width=0.9)
here = star(radius=0.2, fill=STAR, stroke=STAR, rays=6, inner_fraction=0.2)
# turns
turns = [
    (blk,7,6), (wht,4,2), (blk,3,4), (wht,7,3), (blk,2,2),
    (wht,3,6), (blk,5,5), (wht,6,6), (blk,6,5), (wht,4,4),
]
# create display
pieces = []
locations = []
for number, turn in enumerate(turns):
    pieces = pieces + [turn[0]]
    locations = locations + [(turn[1], turn[2])]
    Grid(x=0.45, y=0.45, fill=TAN, stroke=LINE, side=1, rows=7, cols=7)
    Rectangle(x=0.45, y=0.45, stroke=LINE, fill=None, height=7.05, width=7.05,
              borders=[('n s', 3, "#967C56"), ('e w', 3, "white")])
    Text(x=4.25, y=0.3, font_size=12, stroke=LINE,
         text="Snex #" + str(number + 1))
    Layout(rect, shapes=pieces, locations=locations)  # all pieces
    Layout(rect, shapes=[here], locations=[(turn[1], turn[2])])  # flash
    PageBreak()
# output to PDF and GIF
Save(
    output='gif',
    directory="../docs/source/examples/images/boards/abstract/",
    dpi=150,
    framerate=1)
