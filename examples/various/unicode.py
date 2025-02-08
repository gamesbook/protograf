# -*- coding: utf-8 -*-
"""
Example Unicode symbols for protograf

Written by: Derek Hohls
Created on: 19 September 2024
"""
from protograf import *

Create(filename="unicode.pdf", margin=1, margin_top=0.25)

header = Common(x=0, y=27, font_size=24, align="left")
header_font = Common(font_size=18, align="left")

Text(common=header, text=r"Unicode Text: Prefix the number with \\u")

Text(common=header_font, x=2, y=25,
     text="\u2248 ...  2248 ... approximately")
Text(common=header_font, x=2, y=24,
     text="\u2022 ...   2022 ... bullet")
Text(common=header_font, x=2, y=23,
     text="\u2713 ...  2713 ... checkmark")
Text(common=header_font, x=2, y=22,
     text="\u2663 ...  2663 ... club")
Text(common=header_font, x=2, y=21,
     text="\u00b3 ...   00B3 ... cubed")
Text(common=header_font, x=2, y=20,
     text="\u2714 ...  2717 ... dark check")
Text(common=header_font, x=2, y=19,
     text="\u00b0 ...   00B0 ... degree")
Text(common=header_font, x=2, y=18,
     text="\u2666 ...  2666 ... diamond")
Text(common=header_font, x=2, y=17,
     text="\u2014 ... 2014 ... em-dash")
Text(common=header_font, x=2, y=16,
     text="\u2709 ...  2709 ... envelope")
Text(common=header_font, x=2, y=15,
     text="\u2665 ...  2665 ... heart")
Text(common=header_font, x=2, y=14,
     text="\u270E ...  270E ... pencil")
Text(common=header_font, x=2, y=13,
     text="\u00b1 ...  00B1 ... plus/minus")
Text(common=header_font, x=2, y=12,
     text="\u2707 ...  2707 ... tape")
Text(common=header_font, x=2, y=11,
     text="\u2799 ...  2799 ... right arrow")
Text(common=header_font, x=2, y=10,
     text="\u2744 ...  2744 ... snowflake")
Text(common=header_font, x=2, y=9,
     text="\u2660 ...  2660 ... spade")
Text(common=header_font, x=2, y=8,
     text="\u00B2 ...   00B2 ... squared")
Text(common=header_font, x=2, y=7,
     text="\u2730 ... 2730 ... star")

Save()
