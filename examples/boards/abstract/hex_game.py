"""
"Hex" game board example for protograf

Written by: Derek Hohls
Created on: 8 March 2024
Notes:
"""

from protograf import *

Create(filename="hex_game_board.pdf", margin=0.5, paper=landscape(A4))

# Background Player Areas
RightAngledTriangle(
    x=-1.1, y=10.0, height=9, width=15.35, fill=white, flip="north", hand="east"
)
RightAngledTriangle(
    x=-1.1, y=10.0, height=9, width=15.35, fill=black, flip="south", hand="east"
)
RightAngledTriangle(
    x=29.55, y=10.0, height=9, width=15.35, fill=black, flip="north", hand="west"
)
RightAngledTriangle(
    x=29.55, y=10.0, height=9, width=15.35, fill=white, flip="south", hand="west"
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
