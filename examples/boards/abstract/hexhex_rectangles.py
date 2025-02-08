"""
"HexHex" game board, with inset rectangle, example for protograf

Written by: Derek Hohls
Created on: 30 August 2024
Notes:
"""

from protograf import *

Create(filename="hexhex_board_rectangles.pdf", margin=0.5, paper=A4)

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    stroke=None,
    fill=None,
    height=2.2,
    centre_shape=rectangle(stroke=black, fill=white, width=1.9, height=2.2, stroke_width=2),
    margin_bottom=4,
)

Save(output='png')
