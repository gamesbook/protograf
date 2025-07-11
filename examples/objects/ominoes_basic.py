# -*- coding: utf-8 -*-
"""
Example code for protograf

Written by: Derek Hohls
Created on: 28 June 2025
"""
from protograf import *

Create(filename="pentominoes_basic.pdf",
       paper="A8",
       margin_left=0.5,
       margin_right=0.5,
       margin_bottom=0.5,
       margin_top=0.5)

header = Common(x=0, y=0, font_size=12, align="left")

# ---- basic Pentomino - upper
Blueprint(stroke_width=0.5, subdivisions=1)
Text(common=header, text="Pentomino: Basic")

basics = Common(side=0.5, outline_stroke="black", outline_width=1)

Pentomino(x=0, y=0, letter="I", label="I", common=basics)
Pentomino(x=0.5, y=0, letter="Y", label="Y", common=basics, fill="silver")
Pentomino(x=1.5, y=0, letter="N", label="N", common=basics)
Pentomino(x=2.5, y=0, letter="L", label="L", common=basics, fill="silver")
Pentomino(x=3, y=0, letter="P", label="P", common=basics)

Pentomino(x=0, y=3, letter="W", label="W", common=basics)
Pentomino(x=1, y=2.5, letter="T", label="T", common=basics, fill="silver")
Pentomino(x=2, y=2.5, letter="F", label="F", common=basics)
Pentomino(x=2.5, y=3, letter="V", label="V", common=basics, fill="silver")

Pentomino(x=0, y=5, letter="U", label="U", common=basics)
Pentomino(x=1.5, y=4.5, letter="X", label="X", common=basics, fill="silver")
Pentomino(x=2.5, y=4.5, letter="Z", label="Z", common=basics)
PageBreak()


# ---- basic Pentomino - lower
Blueprint(stroke_width=0.5, subdivisions=1)
Text(common=header, text="Pentomino: Lowercase")
Pentomino(x=0, y=0, letter="i", label="i", common=basics)
Pentomino(x=0.5, y=0, letter="y", label="y", common=basics, fill="silver")
Pentomino(x=1.5, y=0, letter="n", label="n", common=basics)
Pentomino(x=2, y=0.5, letter="l", label="l", common=basics, fill="silver")
Pentomino(x=3, y=0, letter="p", label="p", common=basics)

Pentomino(x=0, y=3, letter="w", label="w", common=basics)
Pentomino(x=1, y=2.5, letter="t", label="t", common=basics, fill="silver")
Pentomino(x=2.5, y=2.5, letter="f", label="f", common=basics)
Pentomino(x=2.5, y=3, letter="v", label="v", common=basics, fill="silver")

Pentomino(x=0, y=5, letter="u", label="u", common=basics)
Pentomino(x=1.5, y=4.5, letter="x", label="x", common=basics, fill="silver")
Pentomino(x=2.5, y=4.5, letter="z", label="z", common=basics)
PageBreak()

# ---- basic Tetromino - upper
Blueprint(stroke_width=0.5, subdivisions=1)
Text(common=header, text="Tetromino: Basic")

tbasics = Common(side=0.75, outline_stroke="black", outline_width=1)

Tetromino(x=0, y=0, letter="I", label="I", common=tbasics)
Tetromino(x=1.5, y=0, letter="S", label="S", common=tbasics)
Tetromino(x=2, y=2, letter="O", label="O", common=tbasics)
Tetromino(x=0, y=3.75, letter="L", label="L", common=tbasics)
Tetromino(x=1.75, y=4, letter="T", label="T", common=tbasics)
PageBreak()

# ---- basic Tetromino - lower
Blueprint(stroke_width=0.5, subdivisions=1)
Text(common=header, text="Tetromino: Lowercase")

tbasics = Common(side=0.75, outline_stroke="black", outline_width=1)

Tetromino(x=0, y=0, letter="i", label="i", common=tbasics)
Tetromino(x=1.5, y=0, letter="s", label="s", common=tbasics)
Tetromino(x=2, y=2, letter="o", label="o", common=tbasics)
Tetromino(x=0, y=3.75, letter="l", label="l", common=tbasics)
Tetromino(x=1.75, y=4, letter="t", label="t", common=tbasics)
PageBreak()


# ---- Tetromino - tetris style
Blueprint(stroke_width=0.5, subdivisions=1)
Text(common=header, text="Tetromino: Tetris")

Tetromino(x=0.5, y=0.5, letter="I", tetris=True, side=0.5)
Tetromino(x=1.5, y=0.5, letter="T", tetris=True, side=0.5)
Tetromino(x=0.5, y=2.5, letter="S", tetris=True, side=0.5)
Tetromino(x=2.5, y=2.5, letter="s", tetris=True, side=0.5)
Tetromino(x=1.5, y=4, letter="O", tetris=True, side=0.5)
Tetromino(x=0.5, y=4, letter="L", tetris=True, side=0.5)
Tetromino(x=2.5, y=4, letter="l", tetris=True, side=0.5)
Tetromino(x=0.5, y=0.5, letter="I", tetris=True, side=0.5)
Tetromino(x=3, y=1.5, letter="*", tetris=True, side=0.5)

Save(
    output='png',
    dpi=300,
    directory="../docs/source/images/objects",
    names=[
        'pentomino_upper',
        'pentomino_lower',
        'tetromino_upper',
        'tetromino_lower',
        'tetromino_tetris',
    ]
)
