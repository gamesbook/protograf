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


# Example from "Games & Puzzles", Issue 9, 1973
basics = Common(fill="silver", side=2, stroke="silver",
                outline_stroke="black", outline_width=1)

Pentomino(x=0, y=0, letter="P", common=basics)
Pentomino(x=0, y=6, letter="T", common=basics)
Pentomino(x=0, y=8, letter="I", common=basics)
Pentomino(x=0, y=16, letter="y", flip="north", common=basics)
Pentomino(x=4, y=0, letter="l", flip="north", common=basics)
Pentomino(x=2, y=2, letter="F", flip="south", common=basics)
Pentomino(x=6, y=2, letter="w", flip="north", common=basics)
Pentomino(x=6, y=6, letter="X", common=basics)
Pentomino(x=2, y=8, letter="n", invert="TB", common=basics)
Pentomino(x=6, y=10, letter="U", common=basics)
Pentomino(x=4, y=14, letter="z", flip="north", common=basics)
Pentomino(x=6, y=14, letter="V", flip="north", common=basics )
PageBreak()

# Example from "Imperial Earth", Arthur C. Clarke, 1975
basics = Common(side=2, stroke=None,
                outline_stroke="black", outline_width=1)
Pentomino(x=0, y=0, letter="N", invert="TB", common=basics)
Pentomino(x=0, y=6, letter="P", invert="TB", common=basics)
Pentomino(x=0, y=12, letter="Y", invert="LR", common=basics)
Pentomino(x=2, y=0, letter="F", flip="north", common=basics)
Pentomino(x=4, y=4, letter="X", side=2, outline_stroke="black", fill="black")
Pentomino(x=4, y=8, letter="U", common=basics)
Pentomino(x=2, y=12, letter="Z",common=basics)
Pentomino(x=2, y=16, letter="l", flip="south", common=basics)
Pentomino(x=4, y=0, letter="V", flip="north", common=basics)
Pentomino(x=10, y=0, letter="I", common=basics)
Pentomino(x=6, y=10, letter="T", flip="south", common=basics)
Pentomino(x=6, y=14, letter="W", flip="north", common=basics)
Text(text='"Imperial Earth"', x=7, y=7.25, stroke="white", font_size=18)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'pentominoes_gp', 'pentominoes_ie'
    ]
)
