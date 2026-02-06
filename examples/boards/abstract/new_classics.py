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

Create(filename="new_classic_boards.pdf", margin=0.5, paper="A4-l")
# common usage
source = '"New Book of Classic Board Games", Brian E. Svoboda, 2026.'
title = Common(x=1, y=1, font_name="Times-Roman", align="left", font_size=13)
credit = Common(x=0.5, y=19.5, font_name="Times-Italic", align="left", font_size=10)

# ---- .Ataxx
Text("Attaxx", common=title)
ATAXX_BLUE = "#21BDE6"
ATX_WALL = "#7C7C7C"
ATX_BLOCK = "#929292"
ATX_SPACE = "#85DBF1"
a00 = '0000000'
xcn = '0001000'
xdb = '0010100'
Polyomino(
    x=1, y=1.5,
    side=0.2,
    pattern=[a00, a00, xcn, xdb, xcn, a00, a00],
    fill=ATX_BLOCK, stroke=ATX_WALL,
)
Polyomino(
    x=3, y=1.5,
    side=0.2,
    pattern=[a00, a00, xcn, '0011100', xcn, a00, a00],
    fill=ATX_BLOCK, stroke=ATX_WALL,
)
Grid(
    x=10, y=1.5,
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
Dot(cx=14.25, cy=9.25, dot_width=5)
Sequence(
    text(text="{{sequence}}", x=0.8, y=9.8, common=HEX_LABELS),
    setting=(1, 11),
    interval_y=0.763, interval_x=1.3,
    )
Sequence(
    text(text="{{sequence}}", x=0.8, y=9.1, common=HEX_LABELS),
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
        # stroke="black",
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
