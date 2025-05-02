# -*- coding: utf-8 -*-
"""
Purpose: Shows all pre-defined SVG colors available from PyMuPDF
Author: Derek Hohls
Created: 2 May 2025
"""
# lib
# local
from protograf import Create, Text, Save, Rectangle
from protograf.utils import support

Create(filename="colorset_svg.pdf")

row, col = 0, 0
svg_colors = support.color_set(True)

for each_color in svg_colors:
    a_color = each_color['name']
    label_color = "black"
    # overwrite label color for dark backgrounds
    if a_color in [
        "midnightblue",
        "navy",
        "darkblue",
        "mediumblue",
        "black",
        "darkslategray",
        "darkslategray",
        "darkred",
        "brown",
        "indigo",
        "teal",
        "blue",
        "green",
        "darkgreen",
        "forestgreen",
        "seagreen",
        "maroon",
        "purple",
        "slateblue",
        "darkslateblue",
    ]:
        label_color = "white"
    Rectangle(row=row, col=col, width=2.7, height=1.25, fill=each_color['hex'])
    Text(
        x=col * 2.7 + 0.1,
        y=row * 1.25 + 0.3,
        font_size=8,
        stroke=label_color,
        align="left",
        text="%s\n%s" % (a_color, each_color['hex']),
    )
    col += 1
    if col > 6:
        col = 0
        row += 1

Text(x=16.25, y=26, text="PyMuPDF: SVG Colors", font_size=14, stroke="red")
Save()
