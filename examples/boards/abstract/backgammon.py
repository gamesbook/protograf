"""
A Backgammon board example for protograf

Written by: Derek Hohls
Created on: 29 December 2024
"""

from protograf import *

Create(filename="backgammon.pdf", margin=1, paper=landscape(A4))

# board outline
Rectangle(x=3, y=0, width=21, height=18, stroke_width=2, fill=burlywood)
# zones background
zone = Common(width=9, height=16, stroke_width=2)
Rectangle(common=zone, x=4, y=1, fill=bisque)
Rectangle(common=zone, x=14, y=1, fill=bisque)
# shared sizes
points = Common(width=1.5, height=7.5, top=0.01)
# left zone
Sequence(
    [trapezoid(common=points, x=4, y=1, fill_stroke=saddlebrown),
     trapezoid(common=points, x=5.5, y=1, fill_stroke=tan)],
    setting=(1, 3), interval_x=3)
Sequence(
    [trapezoid(common=points, x=14, y=1, fill_stroke=saddlebrown),
     trapezoid(common=points, x=15.5, y=1, fill_stroke=tan)],
    setting=(1, 3), interval_x=3)
# right zone
Sequence(
    [trapezoid(common=points, x=4, y=9.5, fill_stroke=tan, flip='s'),
     trapezoid(common=points, x=5.5, y=9.5, fill_stroke=saddlebrown, flip='s')],
    setting=(1, 3), interval_x=3)
Sequence(
    [trapezoid(common=points, x=14, y=9.5, fill_stroke=tan, flip='s'),
     trapezoid(common=points, x=15.5, y=9.5, fill_stroke=saddlebrown, flip='s')],
    setting=(1, 3), interval_x=3)
# zone edges
Rectangle(common=zone, x=4, y=1, fill=None)
Rectangle(common=zone, x=14, y=1, fill=None)

PageBreak()
Save()
