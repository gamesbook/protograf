"""
An Octagons board example for protograf

Written by: Derek Hohls
Created on: 28 December 2024
"""

from protograf import *

Create(filename="octagons.pdf", margin=1.25)

oct_flat = polygon(
    sides=8, x=1.1, y=3.75, width=2.35, height=2.35, stroke_width=2, fill=white,
    perbis='1,5', perbis_stroke_width=2)
oct_vert = polygon(
    sides=8, x=1.1, y=3.75, width=2.35, height=2.35, stroke_width=2, fill=white,
    perbis='3,7', perbis_stroke_width=2)

Trapezoid(x=-0.25, y=2, height=3, width=18, top=14, fill_stroke=grey)
Trapezoid(x=-0.25, y=18, height=3, width=18, top=14, fill_stroke=grey, flip='s')
Polyshape(points=[(-0.25,21), (2,18), (2,5), (-0.25,2)], fill=black)
Polyshape(points=[(17.75,21), (15.75,18), (15.75,5), (17.75,2)], fill=black)

Rectangle(x=1, y=4, height=15, width=16, fill=white)

Repeat(oct_flat, cols=8, rows=8, interval=2.2,
       across=(1, 3, 5, 7), down=(1, 3, 5, 7), offset_x=2.2)
Repeat(oct_vert, cols=8, rows=8, interval=2.2,
       across=(1, 3, 5, 7), down=(1, 3, 5, 7))
Repeat(oct_vert, cols=8, rows=8, interval=2.2,
       across=(2, 4, 6, 8), down=(2, 4, 6, 8))
Repeat(oct_flat, cols=8, rows=8, interval=2.2,
       across=(2, 4, 6, 8), down=(2, 4, 6, 8), offset_x=-2.2)

Save()
