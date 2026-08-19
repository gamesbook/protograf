"""
A Mancala board example for protograf

Written by: Derek Hohls
Created on: 17 August 2026
"""

from protograf import *

Create(
    filename="mancala.pdf",
    paper="A4-l",
    margins=1,
    # page_grid=1
)

# board outline
brd = Rectangle(
    x=4.25, y=4,
    width=20, height=12,
    prows=[("w", 4), ("e", 4)],
    stroke_width=8,
    stroke="#CA865D",
    fill="#8B4837")

# small pit style
smalls = Common(
    radius=1.5, stroke_width=2,
    fill="#7E3B2C", stroke="#CA865D")
# large pit style
larges = Common(
    radius=2.75, stroke_width=3,
    fill="#7E3B2C", stroke="#CA865D")

# small pits in top zone
Repeat(
    circle(common=smalls,
           cx=brd.geo.nw.x + 2.5,
           cy=brd.geo.nw.y + 2),
    cols=6, rows=1,
    interval_x=3)
# small pits in bottom zone
Repeat(
    circle(common=smalls,
           cx=brd.geo.nw.x + 2.5,
           cy=brd.geo.nw.y + 10),
    cols=6, rows=1,
    interval_x=3)

# left, large pit
Circle(
    common=larges,
    cx=brd.geo.nw.x,
    cy=brd.geo.nw.y + 6)
# right, large pit
Circle(
    common=larges,
    cx=brd.geo.nw.x + 20,
    cy=brd.geo.nw.y + 6)

Save()
