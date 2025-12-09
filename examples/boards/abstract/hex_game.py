"""
"Hex" game board example for protograf

Written by: Derek Hohls
Created on: 8 March 2024
Revised on: 23 October 2025
Notes:
"""

from protograf import *

Create(filename="hex_game_board.pdf", margin=0.5, paper="A4-l")

# "Hex" Game Board
Rhombus(
    height=18, width=30.7, cx=14.25, cy=9.25,
    stroke="black", fill="white", stroke_width=1,
    slices=["red", "black", "red", "black"]
)
Hexagons(
    cols=21,
    rows=11,
    hex_layout="diamond",
    height=1.5,
    margin_bottom=1.25,
    margin_left=-0.1,
)

Save()
