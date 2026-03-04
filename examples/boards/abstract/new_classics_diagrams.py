"""
"New Classic" diagrams example for protograf

Written by: Derek Hohls
Created on: 4 March 2026

Notes:

  * The diagrams in this collection are based on those presented in the
    booklet "A NEW BOOK OF CLASSIC BOARD GAMES (V1.0)"  by Brian E. Svoboda
    as discussed here https://boardgamegeek.com/thread/3357842 - but
    any faults, errors or omissions are mine and *not* the author's!

  * The recommended font is Fira Mono - see
    https://fonts.google.com/specimen/Fira+Mono to download and install
    FiraMono-Regular.ttf and FiraMono-Bold.ttf

License:

The text and figures in the book "A NEW BOOK OF CLASSIC BOARD GAMES (V1.0)" are
copyrighted by Brian Svoboda (2024) and released under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International license.  See
https://creativecommons.org/licenses/by-nc-sa/4.0/ for the full license.

This script is released under that same license.
"""

from protograf import *

Create(filename="new_classic_diagrams.pdf", margin=0.5, paper="A6")

# ---- common usage
source = '"New Book of Classic Board Games", Brian E. Svoboda, 2026.'
title = Common(x=4.75, y=11, font_name="Times-Bold", align="centre", font_size=12)
credit = Common(x=1.5, y=13, font_name="Times-Italic", align="left", font_size=9)

# ---- .Ataxx
def attaxx_grid(x=0, y=0, size=1.5):
    board = Grid(
        x=x, y=y,
        cols=3, rows=3,
        side=size,
        fill=ATAXX_BLUE,
        stroke_width=1)
    grid = RectangularLocations(
        x=x+size/2, y=y+size/2,
        cols=3, rows=3,
        interval=size)
    return grid

# Blueprint()
Text("Attaxx: Figure 8.2", common=title)
Text(source, common=credit)
ATAXX_BLUE = "#21BDE6"
# colors/styles
atx = Common(
    fill="#929292",
    stroke="#7C7C7C",
    blank_fill="#85DBF1",
    stroke_width=1,
    side=0.25)
black = Common(
    radius=0.55,fill="#2E2E2E",stroke="black",stroke_width=2,
    label_size=24, label_stroke="red")
white = Common(
    radius=0.55,fill="white",stroke="#2E2E2E",stroke_width=2,
    label_size=24, label_stroke="red")
# boards
brd1 = attaxx_grid(x=0, y=0)
brd2 = attaxx_grid(x=5, y=0)
brd3 = attaxx_grid(x=0, y=5.25)
brd4 = attaxx_grid(x=5, y=5.25)
# pieces
target = circle(radius=0.55,fill="#14A1C4",stroke_width=3,dotted=True)
w1 = circle(common=white)
w1A = circle(common=white, label="A")
b1 = circle(common=black)
b1A = circle(common=black, label="A")
b1B = circle(common=black, label="B")
b_y = circle(common=black, centre_shape=circle(
            radius=0.65,fill=None,stroke="yellow",stroke_width=4,dotted=True))
# show board + pieces
Layout(brd1, locations=[(1,2),(2,2),(3,2)], shapes=[w1,b1A,target])
Layout(brd2, locations=[(1,2),(2,2),(3,2)], shapes=[w1,b1,b1])
Layout(brd3, locations=[(2,1),(3,1),(2,2),(3,2),(1,3),(3,3)], shapes=[w1,w1,target,b1,b1B,w1])
Layout(brd4, locations=[(2,1),(3,1),(2,2),(3,2),(1,3),(3,3)], shapes=[b_y,b_y,b1,b1,b1,b_y])
# extras
Line(x=0, y=4.85, length=9.5, stroke="#BDBDBD", stroke_width=2, dotted=True)
Line(x=4.4, y=2.25, length=0.8, stroke="#7D7D7D", stroke_width=3, arrow_width=0.6)
Line(x=4.4, y=7.5, length=0.8, stroke="#7D7D7D", stroke_width=3, arrow_width=0.6)

Text(source, common=credit)
PageBreak()


Save()
