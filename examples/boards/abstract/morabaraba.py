"""
A Morabaraba board example for protograf

Written by: Derek Hohls
Created on: 1 May 2025

Note:
    * Morabaraba is widely played in South Africa; elsewhere it may be referred
      to as Eleven Men's Morris
"""

from protograf import *

Create(filename="morabaraba.pdf", margin_left=0.5, margin_right=0.5, paper="A4")

# square outlines
rect = Common(cx=10, cy=15, stroke_width=3, fill=None)
r1 = Rectangle(common=rect, width=18, height=18)
Rectangle(common=rect, width=12, height=12)
Rectangle(common=rect, width=6, height=6)
lns = Common(stroke_width=3)
# top half
Line(common=lns, x=1, y=6, x1=7, y1=12)
Line(common=lns, x=10, y=6, x1=10, y1=12)
Line(common=lns, x=19, y=6, x1=13, y1=12)
# middle
Line(common=lns, x=1, y=15, x1=7, y1=15)
Line(common=lns, x=19, y=15, x1=13, y1=15)
# bottom half
Line(common=lns, x=1, y=24, x1=7, y1=18)
Line(common=lns, x=10, y=24, x1=10, y1=18)
Line(common=lns, x=19, y=24, x1=13, y1=18)

Save()
