"""
A chess board example for protograf

Written by: Derek Hohls
Created on: 29 February 2016
Notes:
    Chess font from: http://www.enpassant.dk/chess/fontimg/alpha.htm
"""

from protograf import *

Create(filename="chessboard.pdf", margin=1.25)

rect_fill = rectangle(x=0, y=4, width=2.25, height=2.25, stroke=None, fill=grey)
Repeat(rect_fill, cols=8, rows=8, across=(1, 3, 5, 7), down=(1, 3, 5, 7), interval=2.25)
Repeat(rect_fill, cols=8, rows=8, across=(2, 4, 6, 8), down=(2, 4, 6, 8), interval=2.25)
Rectangle(x=0, y=4, width=18, height=18, stroke_width=3, fill=None)
PageBreak()

sqr = Common(side=2.25, stroke=None)
sqr_locations = RectangularLocations(
    cols=8, rows=8, x=1.25, y=5, interval_x=2.25, interval_y=2.25,
    start="NW", direction="east", pattern="snake")
Layout(
   sqr_locations,
   shapes=[square(common=sqr, fill=white), square(common=sqr, fill=grey)])
Rectangle(x=0.18, y=3.85, width=18, height=18, stroke_width=3, fill=None)

Save()
