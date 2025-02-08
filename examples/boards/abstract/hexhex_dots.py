"""
"HexHex" game board, with dots, example for protograf

Written by: Derek Hohls
Created on: 3 August 2024
Notes:
"""

from protograf import *

Create(filename="hexhex_board_dots.pdf", margin=0.5, paper=A4)

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    stroke=white,
    fill=None,
    height=2.2,
    dot=0.1,
    dot_stroke=gray,
    margin_bottom=4,
)

Save(output='png')
