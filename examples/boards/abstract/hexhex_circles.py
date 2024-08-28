"""
"HexHex" game board, with inset circles, example for pyprototypr

Written by: Derek Hohls
Created on: 3 August 2024
Notes:
"""

from pyprototypr import *

Create(filename="hexhex_board_circles.pdf", margin=0.5, pagesize=A4)

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    stroke=white,
    fill=None,
    height=2.2,
    centre_shape=circle(stroke=black, fill=white, radius=1.1, stroke_width=2),
    margin_bottom=4,
)

Save(output='png')
