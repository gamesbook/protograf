# -*- coding: utf-8 -*-
"""
Example protograf code for creating "real world" art

Written by: Derek Hohls
Created on: 17 September 2025

Source: https://bergerfohr.com/collections/math-2
"""
from protograf import *

Create(
    filename="math-2.pdf",
    margin=1,
    page_grid=1)
Line(x=10, y=5.3, length=4.2, stroke_width=7, stroke="grey")
EquilateralTriangle(cx=5.7, cy=6.2, side=4.3, fill_stroke="yellow")
Square(x=12.2, y=9.5, side=4.1, fill_stroke="green")
Circle(x=6, y=14, radius=2, fill_stroke="blue")
Line(x=10, y=20.0, length=4.2, stroke_width=7, stroke="black",
     wave_style='wave', wave_height=0.25)
Rectangle(x=3.6, y=22.2, height=2.1, width=4.3, fill_stroke="red")
# Image("math2.png", width=19, height=27, x=0, y=0)
Save()
