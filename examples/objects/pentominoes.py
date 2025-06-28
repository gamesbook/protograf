# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 28 June 2025
"""
from protograf import *

Create(filename="pentominoes.pdf",
       paper="A5",
       margin_left=1.25,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

# Blueprint(stroke_width=0.5)
Text(common=header, text="Pentominoes")
basics = Common(fill="silver", side=2)

Pentomino(x=0, y=0, letter="P", rotation=0, common=basics)
Pentomino(x=0, y=6, letter="T", rotation=0, common=basics)
Pentomino(x=0, y=8, letter="I", rotation=0, common=basics)
Pentomino(x=0, y=16, letter="y", rotation=90, common=basics)
Pentomino(x=4, y=0, letter="l", rotation=90, common=basics)
Pentomino(x=2, y=2, letter="F", rotation=-90, common=basics)
Pentomino(x=6, y=2, letter="w", rotation=90, common=basics)
Pentomino(x=6, y=6, letter="X", rotation=0, common=basics)
Pentomino(x=2, y=8, letter="n", rotation=0, invert="TB", common=basics)
Pentomino(x=6, y=10, letter="U", rotation=0, common=basics)
Pentomino(x=4, y=14, letter="z", rotation=90, common=basics)
Pentomino(x=6, y=14, letter="V", rotation=90, common=basics )

Save(
    output='png',
    dpi=300,
    directory="../docs/source/examples/images/objects",
    names=[
        'pentominoes',
    ]
)
