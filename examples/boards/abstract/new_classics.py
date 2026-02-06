"""
"New Classic" game boards example for protograf

Written by: Derek Hohls
Created on: 6 February 2026

Notes:
  * The boards in this collection are based on those presented in the
    booklet "A NEW BOOK OF CLASSIC BOARD GAMES (V1.0)"  by Brian E. Svoboda
    as discussed here https://boardgamegeek.com/thread/3357842 - but
    any faults, errors or omissions are mine and *not* the author's!
"""

from protograf import *

Create(filename="new_classic_boards.pdf", margin=0.5, paper="A4-l", page_grid=1)
# common usage
source = '"New Book of Classic Board Games", Brian E. Svoboda, 2026.'
title = Common(x=1, y=1, font_name="Times-Roman", align="left", font_size=13)
credit = Common(x=0.5, y=19.75, font_name="Times-Italic", align="left", font_size=10)

# ---- .Ataxx
Text("Attaxx", common=title)
ATAXX_BLUE = "#21BDE6"
atx = Common(
    fill="#929292", stroke="#7C7C7C",
    blank_fill="#85DBF1",
    stroke_width=1,side=0.25,)
x00 = '0000000'
xcn = '0001000'
xdb = '0010100'
xot = '1000001'
xin = '0100010'
Polyomino(
    x=2, y=1.5, common=atx,
    pattern=[x00, x00, xcn, xdb, xcn, x00, x00])
Polyomino(
    x=4, y=1.5, common=atx,
    pattern=[x00, x00, xcn, '0011100', xcn, x00, x00])
Polyomino(
    x=6, y=1.5, common=atx,
    pattern=[xdb, x00, '1001001', x00, '1001001', x00, xdb])
Polyomino(
    x=2, y=3.5, common=atx,
    pattern=[x00, x00, xdb, x00, xdb, x00, x00])
Polyomino(
    x=4, y=3.5, common=atx,
    pattern=[x00, xin, xdb, x00, xdb, xin, x00])
Polyomino(
    x=6, y=3.5, common=atx,
    pattern=[xcn, xdb, xin, xot, xin, xdb, xcn])
Polyomino(
    x=2, y=5.5, common=atx,
    pattern=[x00, x00, xdb, xcn, xdb, x00, x00])
Polyomino(
    x=4, y=5.5, common=atx,
    pattern=[xcn, x00, x00, xot, x00, x00, xcn])
Polyomino(
    x=6, y=5.5, common=atx,
    pattern=[xdb, x00, '1010101', x00, '1010101', x00, xdb])
Polyomino(
    x=2, y=7.5, common=atx,
    pattern=[xcn, xcn, x00, '1100011', x00, xcn, xcn])
Polyomino(
    x=4, y=7.5, common=atx,
    pattern=[xcn, xcn, xcn, '1110111', xcn, xcn, xcn])
Polyomino(
    x=6, y=7.5, common=atx,
    pattern=[xdb, xdb, xot, '1001001', xot, xdb, xdb])
Polyomino(
    x=2, y=9.5, common=atx,
    pattern=[x00, xdb, xin, x00, xin, xdb, x00])
Polyomino(
    x=4, y=9.5, common=atx,
    pattern=[xcn, x00, xin, xot, xin, x00, xcn])
Polyomino(
    x=6, y=9.5, common=atx,
    pattern=['0011100', x00, '1101011', xot, '1101011', x00, '0011100'])
Polyomino(
    x=2, y=11.5, common=atx,
    pattern=[xdb, x00, xdb, xin, xdb, x00, xdb])
Polyomino(
    x=4, y=11.5, common=atx,
    pattern=[xdb, xin, xot, x00, xot,xin, xdb])
Polyomino(
    x=6, y=11.5, common=atx,
    pattern=[xcn, x00, '0110110', '1100011', '0110110', x00, xcn])
Polyomino(
    x=2, y=13.5, common=atx,
    pattern=[x00, xdb, '1101011', xcn, '1101011', xdb, x00])
Polyomino(
    x=4, y=13.5, common=atx,
    pattern=[x00, x00, x00, x00, x00, x00, x00])
Grid(
    x=9, y=1.5,
    rows=7, cols=7,
    side=2.5,
    fill=ATAXX_BLUE,
    stroke_width=2
)
Text(source, common=credit)
PageBreak()

# ---- .Cairo Corridor
# ---- .Checkers
# ---- .Chinese Checkers
# ---- .Connect6

# ---- .Go
Text("Go", common=title)
Text(source, common=credit)
Rectangle(
    height=19, width=19,
    x=4.5, y=0.5,
    fill_stroke="#DCB35C")
Grid(
    x=6, y=2,
    cols=8, rows=8,
    stroke_width=1,
    side=2
)
Dot(cx=14, cy=10, dot_width=10)
PageBreak()

# ---- .Hex
Text("Hex", common=title)
Text(source, common=credit)
HEX_LABELS = Common(align="left", font_size=20, stroke="#B58863")
Rhombus(
    height=17, width=29.2, cx=14.25, cy=9.25,
    stroke="black", fill="white", stroke_width=1,
    slices=["white", "black", "white", "black"]
)
Hexagons(
    cols=21, rows=11,
    hex_layout="diamond",
    height=1.5,
    fill="#F0D9B5",
    margin_bottom=1.25,
    margin_left=-0.1,
)
Dot(cx=14.25, cy=9.25, dot_width=6)
Sequence(
    text(text="{{sequence}}",
         x=0.8, y=9.8,
         common=HEX_LABELS),
    setting=(1, 11),
    interval_y=0.763, interval_x=1.3,
    )
Sequence(
    text(text="{{sequence}}",
         x=0.8, y=9.1,
         common=HEX_LABELS),
    setting=('a', 'k', 1, 'letter'),
    interval_y=-0.763, interval_x=1.3,
    )
PageBreak()

# ---- .Joust
# ---- .King's Valley
# ---- .Mills

# ---- .Odd
Text("Odd", common=title)
Text(source, common=credit)
ODD_FRAME = "#FDDCDC"
ODD_BORDER = "#8A1F20"
ODD_FILL = "#ED3436"
Hexagon(cx=14.8, cy=10.5, height=17, fill_stroke=ODD_FRAME)
HexHex(
    cx=14.8, cy=10.5,
    height=1.8,
    rings=4,
    orientation="pointy",
    shape=hexagon(
        height=1.65, orientation="pointy",
        fill=ODD_FILL,
        stroke=ODD_BORDER,
        stroke_width=1)
)
PageBreak()

# ---- .Sea Battle Tafl
# ---- .Sprouts
# ---- .Squava
# ---- .Strands
# ---- .Turkish Checkers
# ---- .Ultimate Tic-Tac-Toe
# ---- .Volo

Save()
