"""
"Meridians" game board example for protograf

Written by: Derek Hohls
Created on: 18 August 2025
Notes:
"""

from protograf import *

Create(filename="meridians.pdf", margin=1, margin_top=4)

Text(text="Meridians", x=3, y=1, font_size=28, rotation=180)
# Hex-shaped, triangle-filled, game board
Hexagon(
    height=17,
    orientation='pointy',
    fill=None,
    stroke_width=2,
    hatch_count=11,
    hatch_stroke_width=2,
)
Text(text="Meridians", align="left", x=14, y=21, font_size=28)

Save()
