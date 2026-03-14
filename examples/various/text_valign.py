# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: R. Martinho Fernandes
Created on: 13 March 2026
"""
from protograf import *

Create(filename="text_valign.pdf", paper="A8", margin=0.5)

properties = Common(
    font_size=5, align="centre", height=0.8, width=0.8, wrap=True, box_stroke="black"
)

Blueprint(stroke_width=0.5)
# Text(common=properties, x=0.1, y=0.1,  text="Top")
Text(common=properties, x=0.1, y=0.1, valign="top", text="Top")
Text(common=properties, x=1.1, y=0.1, valign="top", text="Top\nTop")
Text(common=properties, x=0.1, y=1.1, valign="middle", text="Middle")
Text(common=properties, x=1.1, y=1.1, valign="middle", text="Middle\nMiddle")
Text(common=properties, x=0.1, y=2.1, valign="bottom", text="Bottom")
Text(common=properties, x=1.1, y=2.1, valign="bottom", text="Bottom\nBottom")

Save()
