# -*- coding: utf-8 -*-
"""
Logo for protograf (aka "eat your own dogfood")

Written by: Derek Hohls
Created on: 5 January 2025
Updated on: 1 June 2025

Notes:
    Not sure what font to use for your logo ... watch
    https://www.youtube.com/watch?v=j7SByXWWVzU
"""
from protograf import Create, Font, Hexagon, Polygon, Text, Save

Create(filename="logo.pdf",
       paper="A8-l",
       margin_left=0.5,
       margin_right=0.3,
       margin_bottom=0.2,
       margin_top=0.5)

sanserif = Font("Courier", size=24, stroke="#3085AC")
Text(x=0, y=1, text='proto', width=3, height=2,
     wrap=True, align="left", stroke="#3085AC")
Text(x=1.72, y=1.1, width=3, height=2,
     text="""<span style="font-family: Helvetica; font-size: 20pt; color: #3085AC">
     <b>graf</b></span>""",
     html=True)
Hexagon(
    cx=1.27, cy=1.61,
    stroke="#3085AC",
    stroke_width=1.1,
    dot=0.03,
    radius=0.2,
)
Polygon(
    cx=2.29, cy=1.61,
    stroke="#3085AC",
    stroke_width=1.1,
    radius=0.2,
    radii='*',
    radii_stroke_width=0.5,
    sides=8
)
Text(x=-2.1, y=2, 
     width=8, height=2,
     text="""
     <span style="font-family:Helvetica; font-size:6.8pt; color:#3085AC; text-align:left">
     <b>making prototypes&#8212;made simple</b></span>""",
     html=True)

Save(
    output='png',
    directory="../docs/source/examples/images/various"
)

# Option for resizable version
# Save(output='svg',
#      dpi=300,
#      directory="/tmp/demo")
