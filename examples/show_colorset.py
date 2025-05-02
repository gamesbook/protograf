# -*- coding: utf-8 -*-
"""
Purpose: Shows all pre-defined colors available from PyMuPDF
Author: Derek Hohls
Created: 2 May 2025
"""
from protograf import *
from protograf.utils import support

Create(filename="colorset.pdf")

Data(source=support.color_set())

Deck(width=2.7, height=1.25)

block = rectangle(x=0, y=0, width=2.7, height=1.25, fill=T('{{name}}'))
label = text(
    x=0.1,
    y=0.3,
    font_size=8,
    stroke="black",
    align="left",
    text=T('{{name}}')
)
col = text(
    x=0.1,
    y=0.6,
    font_size=8,
    stroke="black",
    align="left",
    text=T('{{hex}}')
)

Card('*', block, label, col)

Save()
