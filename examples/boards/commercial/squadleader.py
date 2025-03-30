"""
A `wargame board` example for protograf

Written by: Derek Hohls
Created on: 21 February 2024
Notes:
"""

from protograf import *

Create(
    filename="squadleader.pdf",
    margin=0.5, margin_bottom=0,
    paper="A4-l")

# set primary color
empty_hex = "darkseagreen"
# background
Rectangle(x=-0.05, y=0.0, width=29, height=19.93, stroke=empty_hex, fill=empty_hex)
# map
Hexagons(
    cols=17,
    rows=10,
    side=1.15,
    stroke="black",
    fill=empty_hex,
    y=0.0,
    x=0.0,
    dot=0.04,
    dot_stroke="white",
    coord_elevation="t",
    coord_type_x="upper",
    coord_font_size=7,
    coord_padding=0,
)
# cover "extra" hexagons
Rectangle(x=-0.05, y=19.95, width=29, height=1, stroke="white", fill="white")
Rectangle(x=28.75, y=0, width=0.6, height=24.93, stroke="white", fill="white")

Save()
