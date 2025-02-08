"""
"HexHex" game board example for protograf

Written by: Derek Hohls
Created on: 3 August 2024
Notes:
"""

from protograf import *

Create(filename="hexhex_board.pdf", margin=0.5, paper=A4)

# Game Board
Hexagons(
    sides=4,
    hex_layout="circle",
    fill=white,
    stroke=black,
    height=2.2,
    margin_bottom=0.5,
    margin_left=0.5,
)

Save()
