"""
"Arbiters" game board example for protograf

Written by: Derek Hohls
Created on: 30 Nov 2025
Notes:
"""

from protograf import *

Create(filename="arbiters_board.pdf", margin=0.25, paper="A3")

# Game Board
Hexagons(
    sides=5,
    hex_layout="circle",
    fill="white",
    stroke="black",
    stroke_width=2,
    side=2,
)

Save(output="png")
