"""
"Dejarik" game board example for protograf

Written by: Derek Hohls
Created on: 9 December 2025
Notes:
"""

from protograf import *

Create(filename="dejarik_board.pdf", margin=0.15, paper="Letter")

Circle(
    cx=10.5, cy=14,
    radius=10,
    stroke_width=20,
    slices=["black", "silver"]*6,
    centre_shapes=[
        circle(radius=6.5, stroke_width=15, slices=["#E0DFDD", "black"]*6, rotation=15),
        circle(radius=2.5, stroke_width=10, fill="silver") 
    ],
    rotation=15
)

Save()
