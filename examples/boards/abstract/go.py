"""
A Go board example for protograf

Written by: Derek Hohls
Created on: 28 December 2024
"""

from protograf import *

Create(filename="go.pdf", margin=1.5)

Grid(
    cols=18, rows=18,
    stroke_width=1
)
# handicap points
DotGrid(
    offset_x=4.5, offset_y=4.5,
    side=6,
    cols=3, rows=3,
    dot_point=8
)

Save()
