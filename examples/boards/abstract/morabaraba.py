"""
A Morabaraba board example for protograf

Written by: Derek Hohls
Created on: 1 May 2025
Updated on: 2 February 2026

Notes:

* Morabaraba is widely played in South Africa; elsewhere it may be
  referred to as Eleven Men's Morris
* By changing the value of SIZE in this script, you can make a bigger,
  or smaller, board
"""

from protograf import *

Create(filename="morabaraba.pdf",
       margin_left=0.5, margin_right=0.5,
       paper="A4")

# square outlines
SIZE = 6
rect = Common(cx=10, cy=14, stroke_width=3, fill=None)
r1 = Rectangle(common=rect, width=SIZE*3, height=SIZE*3)
r2 = Rectangle(common=rect, width=SIZE*2, height=SIZE*2)
r3 = Rectangle(common=rect, width=SIZE, height=SIZE)
# vertex links (diagonal)
lns = Common(stroke_width=3)
Line(common=lns, links=[r3.geo.ne, r1.geo.ne])
Line(common=lns, links=[r3.geo.nw, r1.geo.nw])
Line(common=lns, links=[r3.geo.se, r1.geo.se])
Line(common=lns, links=[r3.geo.sw, r1.geo.sw])
# perbis links (orthogonal)
Line(common=lns, links=[r3.geo.n, r1.geo.n])
Line(common=lns, links=[r3.geo.s, r1.geo.s])
Line(common=lns, links=[r3.geo.e, r1.geo.e])
Line(common=lns, links=[r3.geo.w, r1.geo.w])

Save()
