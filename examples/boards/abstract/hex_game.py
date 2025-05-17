"""
"Hex" game board example for protograf

Written by: Derek Hohls
Created on: 8 March 2024
Notes:
"""

from protograf import *

Create(filename="hex_game_board.pdf", margin=0.5, paper="A4-l")

# Background Player Areas
locale = Common(y=9.25, height=9, width=15.35)
RightAngledTriangle(
    common=locale, x=-1.1,  fill="white", flip="north", hand="east"
)
RightAngledTriangle(
    common=locale, x=-1.1, fill="black", flip="south", hand="east"
)
RightAngledTriangle(
    common=locale, x=29.55, fill="black", flip="north", hand="west"
)
RightAngledTriangle(
    common=locale, x=29.55, fill="white", flip="south", hand="west"
)

# Hex Game Board
Hexagons(
    cols=21,
    rows=11,
    hex_layout="diamond",
    height=1.5,
    margin_bottom=1.25,
    margin_left=-0.1,
)

Save()
