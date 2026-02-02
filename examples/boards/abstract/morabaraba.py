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
lns = Common(stroke_width=3)
# vertex connections (diagonal)
Line(common=lns, connections=[(r3, 'v', 'ne'), (r1, 'v', 'ne')])
Line(common=lns, connections=[(r3, 'v', 'nw'), (r1, 'v', 'nw')])
Line(common=lns, connections=[(r3, 'v', 'se'), (r1, 'v', 'se')])
Line(common=lns, connections=[(r3, 'v', 'sw'), (r1, 'v', 'sw')])
# perbis connections (orthoganal)
Line(common=lns, connections=[(r3, 'p', 'n'), (r1, 'p', 'n')])
Line(common=lns, connections=[(r3, 'p', 's'), (r1, 'p', 's')])
Line(common=lns, connections=[(r3, 'p', 'e'), (r1, 'p', 'e')])
Line(common=lns, connections=[(r3, 'p', 'w'), (r1, 'p', 'w')])

Save()
