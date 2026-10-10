"""
Written by: Derek Hohls
Created on: 9 Oct 2026
"""
from protograf import *
from protograf.shapes import HexHexLocations

Create(
    paper_height=20,
    paper_width=20,
    margin=1,
    stroke_width=0.5,
    page_grid=1,
    page_grid_dark=5,
    show_margins=True,
)
txt = Common(x=0, y=0, font_size=12, align="left")
header = Common(x=0, y=0, font_size=12, align="left")
diagram= Common(font_size=12, align="centre")

# ---- Hexagonal Grid Labels
games = Common(
    name="hexhex",
    height=1.5,
    hexes=4,
    label=True,
    label_size=12,
)

abl = AbstractGame(
    common=games,
    x=0, y=0,
    label_start='BL',
    )
AbstractState(board=abl)
Text("HexHex: label BL", x=4, y=8, common=diagram)

abr = AbstractGame(
    common=games,
    x=10, y=0,
    label_start='BR',
    )
AbstractState(board=abr)
Text("HexHex: label BR", x=14, y=8, common=diagram)

atl = AbstractGame(
    common=games,
    x=0, y=10,
    label_start='TL',
    )
AbstractState(board=atl)
Text("HexHex: label TL", x=4, y=18, common=diagram)

atr = AbstractGame(
    common=games,
    x=10, y=10,
    label_start='TR',
    )
AbstractState(board=atr)
Text("HexHex: label TR", x=14, y=18, common=diagram)

PageBreak()
# Hexagons(
#     x=10, y=10,
#     height=1,
#     rows=5, cols=5,
#     stroke_width=1,
#     orientation="pointy"
# )

# ---- Rectangular Grid Labels
gridded = Common(
    name="grid",
    height=1.5,
    rows=6,
    cols=7,
    label=True,
    label_size=12,
)

agbl = AbstractGame(
    common=gridded,
    x=1, y=0,
    label_start='BL',
    )
AbstractState(board=agbl)
Text("Grid: label BL", x=4, y=8, common=diagram)

agbr = AbstractGame(
    common=gridded,
    x=11, y=0,
    label_start='BR',
    )
AbstractState(board=agbr)
Text("Grid: label BR", x=14, y=8, common=diagram)

agtl = AbstractGame(
    common=gridded,
    x=1, y=11,
    label_start='TL',
    )
AbstractState(board=agtl)
Text("Grid: label TL", x=4, y=18, common=diagram)

agtr = AbstractGame(
    common=gridded,
    x=11, y=11,
    label_start='TR',
    )
AbstractState(board=agtr)
Text("Grid: label TR", x=14, y=18, common=diagram)


Save()
