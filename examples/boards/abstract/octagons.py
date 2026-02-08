"""
An Octagons board example for protograf

Written by: Derek Hohls
Created on: 28 December 2024
"""

from protograf import *

Create(filename="octagons.pdf", margin=1.25)

oct_flat = polygon(
    sides=8, x=1.1, y=3.75,
    width=2.35, height=2.35,
    stroke_width=2, fill="white",
    perbii='4,8', perbii_stroke_width=2)
oct_vert = polygon(
    sides=8, x=1.1, y=3.75,
    width=2.35, height=2.35,
    stroke_width=2, fill="white",
    perbii='2,6', perbii_stroke_width=2)

# background/edge
Rectangle(
    x=-0.25, y=2.5,
    height=18, width=18,
    slices=['black', 'black', 'gray', 'gray'],
    fill=None,
    stroke="white")
Rectangle(x=1.25, y=4, height=15, width=15.25, fill="white")
# main board
Repeat(oct_flat, cols=8, rows=8, interval=2.2,
       across=(1, 3, 5, 7), down=(1, 3, 5, 7), offset_x=2.2)
Repeat(oct_vert, cols=8, rows=8, interval=2.2,
       across=(1, 3, 5, 7), down=(1, 3, 5, 7))
Repeat(oct_vert, cols=8, rows=8, interval=2.2,
       across=(2, 4, 6, 8), down=(2, 4, 6, 8))
Repeat(oct_flat, cols=8, rows=8, interval=2.2,
       across=(2, 4, 6, 8), down=(2, 4, 6, 8), offset_x=-2.2)
Save()
